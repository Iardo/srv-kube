#!/usr/bin/env python3

'''
Runs the Docker Compose integration tests for every service under "serv/".

Each service has its own test in test/task/int/test_<service>.py. Running
one spins up that service's containers with docker compose, waits for them
to reach a running (and healthy, where applicable) state, then tears
everything back down. Requires Docker with a running daemon.

These are integration tests, not unit tests - they exercise real containers,
volumes and the Docker daemon rather than isolated code. Services run
concurrently (see --jobs) since each one is fully isolated (its own compose
project, network and dynamically-reserved host ports), which is what makes
a full run of ~40 services practical instead of a long serial queue.
'''

import argparse
import concurrent.futures
import datetime
import importlib
import os
import shutil
import subprocess
import sys
import threading
import time
import unittest

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from test.util import engine

TEST_DIR = os.path.join(REPO_ROOT, 'test', 'task', 'int')
LOG_DIR = os.path.join(REPO_ROOT, 'logs', 'test')
SERV_DIR = os.path.join(REPO_ROOT, 'serv')
# Where each run's throwaway copy of serv/ goes - temp/serv-<date>-<epoch>,
# named per-run rather than reused, so a leftover directory a container
# wrote root-owned files into (which this user can't delete without sudo)
# never blocks or gets merged into by a later run.
TEMP_SERV_PARENT = os.path.join(REPO_ROOT, 'temp')

# Leaves one core free for the rest of the machine rather than saturating it.
DEFAULT_JOBS = max(1, (os.cpu_count() or 2) - 1)
# The live "Running:" block only ever shows this many services at once, even
# if more than that are actually executing in the background - keeps that
# part of the display a fixed, small size instead of one line per service.
# Finished services aren't limited by this: each one prints permanently once
# done and stays in the terminal's normal scrollback.
MAX_VISIBLE_SLOTS = 4

SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


class Ansi:
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'
    CLEAR_TO_END = '\033[J'


def discover_services():
    services = []
    for name in sorted(os.listdir(TEST_DIR)):
        if name.startswith('test_') and name.endswith('.py'):
            services.append(name[len('test_'):-len('.py')])
    return services


def docker_available():
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True)
    except FileNotFoundError:
        return False
    return result.returncode == 0


def _tolerant_copy(src, dst, *, follow_symlinks=True):
    '''
    Some services accumulate root-owned runtime files from previous
    container runs (a redis dump.rdb, a generated TLS key, a database
    file) that the current user can't read. Those are stale data, not part
    of the service definition, so skip them with a warning instead of
    aborting the whole copy.
    '''
    try:
        shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    except PermissionError:
        print(f'(skipping unreadable file: {src})', file=sys.stderr)


def prepare_temp_serv():
    '''
    Copies serv/ to a fresh temp/serv-<date>-<epoch>/ and points the engine
    at the copy, so any directories a service's init.sh or docker-compose.yml
    creates land there instead of in the real repo. Returns the directory
    actually used.

    Named per-run rather than reused: a container that ran as root can
    leave files behind this user can't delete without sudo, and reusing
    such a directory fails outright (even copytree's own metadata-copying
    trips over a directory it doesn't own). Naming it after the current
    date and time instead means every run gets a clean directory with
    essentially no chance of colliding with a previous one - the tiny
    remaining chance (two runs in the same second) falls back to a PID
    suffix.
    '''
    now = datetime.datetime.now()
    target = os.path.join(TEMP_SERV_PARENT, f'serv-{now.strftime("%Y%m%d")}-{int(now.timestamp())}')
    if os.path.exists(target):
        target = f'{target}-{os.getpid()}'

    shutil.copytree(SERV_DIR, target, copy_function=_tolerant_copy)
    engine.SERV_DIR = target
    return target


def cleanup_temp_serv(target):
    shutil.rmtree(target, ignore_errors=True)


def load_test_case(service):
    '''Finds the ComposeIntegrationTestCase subclass defined in test_<service>.py.'''
    module_name = f'test.task.int.test_{service}'
    module = importlib.import_module(module_name)
    for attr in vars(module).values():
        if (
            isinstance(attr, type)
            and issubclass(attr, engine.ComposeIntegrationTestCase)
            and attr.__module__ == module_name
        ):
            return attr
    raise LookupError(f'no test case found in {module_name}')


class Line:
    def __init__(self, service):
        self.service = service
        self.state = 'running'  # running, pass, fail, skip
        self.duration = None
        self.message = None
        self.spin_index = 0


def colorize(text, color, enabled):
    if not enabled or not text:
        return text
    return f'{color}{text}{Ansi.RESET}'


def format_duration(seconds):
    '''Formats a duration as human-readable "1h 2m 3s 45ms", dropping leading zero units.'''
    total_ms = round(max(0.0, seconds) * 1000)
    hours, remainder_ms = divmod(total_ms, 3_600_000)
    minutes, remainder_ms = divmod(remainder_ms, 60_000)
    secs, ms = divmod(remainder_ms, 1000)

    parts = []
    if hours:
        parts.append(f'{hours}h')
    if hours or minutes:
        parts.append(f'{minutes}m')
    if hours or minutes or secs:
        parts.append(f'{secs}s')
    parts.append(f'{ms}ms')
    return ' '.join(parts)


def last_meaningful_line(message):
    '''Picks the single most useful line for the compact view - the full detail always goes to the log file.'''
    if not message:
        return ''
    lines = [line.strip() for line in message.strip().splitlines() if line.strip()]
    if not lines:
        return ''
    for line in lines:
        if 'Error:' in line:
            return line
    for line in lines:
        if 'state=' in line:
            return line
    return lines[-1]


def render_line(line, width, color):
    symbol_plain, symbol_color = {
        'running': (SPINNER_FRAMES[line.spin_index % len(SPINNER_FRAMES)], Ansi.YELLOW),
        'pass': ('✓', Ansi.GREEN),
        'fail': ('✗', Ansi.RED),
        'skip': ('-', Ansi.GRAY),
    }[line.state]

    base = f'{symbol_plain} {line.service}'
    if line.duration is not None:
        base += f' ({format_duration(line.duration)})'

    extra = ''
    if line.state == 'fail' and line.message:
        extra = '  ' + last_meaningful_line(line.message)
    elif line.state == 'skip' and line.message:
        extra = '  ' + line.message.strip()

    budget = max(0, width - len(base) - 1)
    if len(extra) > budget:
        extra = (extra[:max(0, budget - 1)] + '…') if budget > 1 else ''

    row = colorize(symbol_plain, symbol_color, color) + f' {line.service}'
    if line.duration is not None:
        row += colorize(f' ({format_duration(line.duration)})', Ansi.GRAY, color)
    if extra:
        row += colorize(extra, Ansi.RED if line.state == 'fail' else Ansi.GRAY, color)
    return row


class ProgressState:
    '''Shared, lock-protected state the render loop and worker threads both touch.'''

    def __init__(self, total, jobs):
        self.total = total
        self.jobs = jobs
        self.lock = threading.Lock()
        self.running = {}   # service -> Line, in start order
        self.done = []       # Line, in completion order

    def start(self, service):
        with self.lock:
            self.running[service] = Line(service)

    def finish(self, service, status, message, duration):
        with self.lock:
            line = self.running.pop(service)
            line.state = status
            line.message = message
            line.duration = duration
            self.done.append(line)
        return line

    def snapshot(self):
        with self.lock:
            return list(self.running.values()), list(self.done)

    def tick_spinners(self):
        with self.lock:
            for line in self.running.values():
                line.spin_index += 1


class Renderer:
    '''
    A sticky footer, not a full-screen view: each finished service prints
    once and stays put in the terminal's normal scrollback (so by the end
    the complete list of every service tested is right there to scroll
    back through), while a small fixed block - a header line plus up to
    MAX_VISIBLE_SLOTS currently-running services - redraws in place at the
    bottom, below whatever's already been printed. Falls back to a plain
    print-as-you-go log when stdout isn't a real terminal (piped output,
    CI logs), where cursor-positioning escape codes don't make sense.
    '''

    def __init__(self, state):
        self.state = state
        self.is_tty = sys.stdout.isatty()
        self._stop = threading.Event()
        self._thread = None
        self._draw_lock = threading.Lock()
        self._footer_line_count = 0

    def start(self):
        if not self.is_tty:
            return
        sys.stdout.write(Ansi.HIDE_CURSOR)
        with self._draw_lock:
            self._draw_footer_locked()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _footer_rows(self, width):
        running, done = self.state.snapshot()
        passed = sum(1 for line in done if line.state == 'pass')
        failed = sum(1 for line in done if line.state == 'fail')
        skipped = sum(1 for line in done if line.state == 'skip')

        rows = [
            f'{len(done)}/{self.state.total} done'
            + colorize(f'  ✓{passed}', Ansi.GREEN, True)
            + colorize(f'  ✗{failed}', Ansi.RED, True)
            + colorize(f'  -{skipped}', Ansi.GRAY, True)
            + colorize(f'  ({self.state.jobs} parallel job(s))', Ansi.GRAY, True),
        ]

        visible = running[:MAX_VISIBLE_SLOTS]
        for line in visible:
            rows.append('  ' + render_line(line, width - 2, True))
        for _ in range(MAX_VISIBLE_SLOTS - len(visible)):
            rows.append(colorize('  (idle)', Ansi.GRAY, True))
        if len(running) > MAX_VISIBLE_SLOTS:
            rows.append(colorize(f'  … and {len(running) - MAX_VISIBLE_SLOTS} more running', Ansi.GRAY, True))

        # Each row's variable-length part is already truncated to width by
        # render_line() before colorizing - truncating again here by raw
        # character count would cut straight through an ANSI escape code,
        # leaving a dangling color that bleeds into whatever prints next.
        return rows

    def _draw_footer_locked(self):
        width = shutil.get_terminal_size((100, 20)).columns
        rows = self._footer_rows(width)
        if self._footer_line_count:
            sys.stdout.write(f'\033[{self._footer_line_count}A')
        sys.stdout.write('\n'.join(f'\033[2K{row}' for row in rows) + '\n')
        sys.stdout.flush()
        self._footer_line_count = len(rows)

    def _loop(self):
        while not self._stop.wait(0.1):
            self.state.tick_spinners()
            with self._draw_lock:
                self._draw_footer_locked()

    def mark_start(self, service):
        self.state.start(service)
        if not self.is_tty:
            print(f'… {service}')

    def mark_done(self, service, status, message, duration):
        line = self.state.finish(service, status, message, duration)
        if not self.is_tty:
            print(render_line(line, 10_000, False))
            return
        with self._draw_lock:
            # Erase the footer entirely, print the now-finished service as
            # a permanent line where the footer used to be, then redraw a
            # fresh footer below it.
            if self._footer_line_count:
                sys.stdout.write(f'\033[{self._footer_line_count}A{Ansi.CLEAR_TO_END}')
            print(render_line(line, 10_000, True))
            self._footer_line_count = 0
            self._draw_footer_locked()

    def stop(self):
        if self._thread:
            self._stop.set()
            self._thread.join()
            sys.stdout.write(Ansi.SHOW_CURSOR)
            sys.stdout.flush()


def run_one(service, timeout_override):
    cls = load_test_case(service)
    if timeout_override:
        cls.timeout = timeout_override

    test = cls('test_containers_start_and_stay_up')
    result = unittest.TestResult()
    start = time.time()
    test.run(result)
    duration = time.time() - start

    if result.skipped:
        return 'skip', result.skipped[0][1], duration
    if result.wasSuccessful():
        return 'pass', None, duration
    problems = result.failures + result.errors
    return 'fail', problems[0][1] if problems else 'unknown failure', duration


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--only', type=str, default=None,
        help='comma-separated services to run, e.g. --only outline,authentik',
    )
    parser.add_argument(
        '--timeout', type=int, default=None,
        help="seconds to wait for a service's containers to become healthy (default: 150)",
    )
    parser.add_argument(
        '-j', '--jobs', type=int, default=DEFAULT_JOBS,
        help=f'how many services to test concurrently (default: cpu count - 1 = {DEFAULT_JOBS} on this machine)',
    )
    parser.add_argument(
        '--list', action='store_true',
        help='list discovered services and exit',
    )
    parser.add_argument(
        '--failfast', action='store_true',
        help="don't start new services once one has failed",
    )
    parser.add_argument(
        '--keep-temp', action='store_true',
        help="don't delete the temp/serv-<date>-<epoch> copy when done, so you can inspect it and clean it up yourself",
    )
    return parser.parse_args()


def resolve_services(all_services, only):
    if not only:
        return all_services

    wanted = [name.strip().replace('-', '_') for name in only.split(',') if name.strip()]
    unknown = set(wanted) - set(all_services)
    if unknown:
        print(f'unknown service(s): {", ".join(sorted(unknown))}', file=sys.stderr)
        print(f'available: {", ".join(all_services)}', file=sys.stderr)
        return None
    return wanted


class FailureLog:
    '''
    Logs each failed service to logs/test/int-<date>-<epoch>.log as soon as
    it fails, not batched up until the whole run finishes - if the run gets
    killed or interrupted partway through (a stuck service, an impatient
    Ctrl+C), whatever already failed is still safely on disk instead of
    vanishing because the final write-out never got a chance to run.
    '''

    def __init__(self):
        self._lock = threading.Lock()
        self.path = None

    def record(self, service, message):
        with self._lock:
            if self.path is None:
                os.makedirs(LOG_DIR, exist_ok=True)
                now = datetime.datetime.now()
                self.path = os.path.join(LOG_DIR, f'int-{now.strftime("%Y%m%d")}-{int(now.timestamp())}.log')
            with open(self.path, 'a') as handle:
                handle.write(f'=== {service} ===\n')
                handle.write(message or '(no details)')
                handle.write('\n\n')


def main():
    args = parse_args()
    all_services = discover_services()

    if args.list:
        for service in all_services:
            print(service)
        return 0

    if not docker_available():
        print('Docker does not seem to be available (is the daemon running?)', file=sys.stderr)
        return 2

    services = resolve_services(all_services, args.only)
    if services is None:
        return 2

    jobs = max(1, args.jobs)
    state = ProgressState(total=len(services), jobs=jobs)
    renderer = Renderer(state)
    failure_log = FailureLog()
    temp_dir = None

    try:
        temp_dir = prepare_temp_serv()
        renderer.start()

        aborted = threading.Event()
        outcomes = {}
        started = time.time()

        def worker(service):
            if aborted.is_set():
                renderer.mark_start(service)
                renderer.mark_done(service, 'skip', 'cancelled (failfast)', 0.0)
                outcomes[service] = ('skip', 'cancelled (failfast)', 0.0)
                return
            renderer.mark_start(service)
            status, message, duration = run_one(service, args.timeout)
            renderer.mark_done(service, status, message, duration)
            outcomes[service] = (status, message, duration)
            if status == 'fail':
                failure_log.record(service, message)
                if args.failfast:
                    aborted.set()

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
                list(pool.map(worker, services))
        finally:
            renderer.stop()
    finally:
        if temp_dir:
            if args.keep_temp:
                print(f'\n(kept temp copy for inspection: {temp_dir})')
            else:
                cleanup_temp_serv(temp_dir)

    # Single prune after the whole run, not per-service - avoids a prune on
    # one thread racing an image pull still in flight on another.
    subprocess.run(['docker', 'image', 'prune', '-a', '-f'], capture_output=True)

    total_duration = time.time() - started
    passed = sum(1 for status, _, _ in outcomes.values() if status == 'pass')
    failed = sum(1 for status, _, _ in outcomes.values() if status == 'fail')
    skipped = sum(1 for status, _, _ in outcomes.values() if status == 'skip')
    color = sys.stdout.isatty()

    print()
    print(colorize('i', Ansi.BLUE, color) + f' tests {len(outcomes)}')
    print(colorize('i', Ansi.BLUE, color) + f' pass {passed}')
    print(colorize('i', Ansi.BLUE, color) + f' fail {failed}')
    print(colorize('i', Ansi.BLUE, color) + f' skipped {skipped}')
    print(colorize('i', Ansi.BLUE, color) + f' duration {format_duration(total_duration)}')

    if failure_log.path:
        print(f'\n{failed} service(s) failed - details logged to {failure_log.path}')

    missing = engine.missing_from_sample()
    if missing:
        print(f'\n{colorize("!", Ansi.YELLOW, color)} host/@host-sample/.env is missing {len(missing)} variable(s) used by tests (a random free port was used instead):')
        for var, needed_by in sorted(missing.items()):
            print(f'  - {var}  (needed by: {", ".join(needed_by)})')

    init_failures = engine.init_script_failures()
    if init_failures:
        print(f'\n{colorize("!", Ansi.YELLOW, color)} init.sh failed for {len(init_failures)} service(s):')
        for service, (returncode, stderr) in sorted(init_failures.items()):
            detail = stderr.strip().splitlines()[-1] if stderr.strip() else f'exit code {returncode}'
            print(f'  - {service}: {detail}')

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
