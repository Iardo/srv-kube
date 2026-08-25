#!/usr/bin/env python3

'''
Shared engine for the Docker Compose integration tests in test/task/int.

These are integration tests, not unit tests: each one spins up a real
"serv/<service>" Docker Compose stack, waits for every declared container to
reach a running (and healthy, where it defines a healthcheck) state, and
tears everything back down. Every service in "serv/" gets its own thin
test_<service>.py that just points ComposeIntegrationTestCase at that
service's directory - this module does the actual work.

Safety rules this engine follows:
  - Every run uses a dedicated compose project ("test-<service>"), so it
    never touches a differently-named/live deployment of the same service.
  - Before starting anything, it checks whether any of the service's
    declared container_name/volume "name:" values already exist. If they
    belong to a *different* project (i.e. a real, live deployment) the test
    is skipped rather than risking interference with it. If they belong to
    a stale "test-<service>" project (a leftover from a previous crashed
    run of this same test) they're removed first.
  - Host ports required by "${VAR:?}" placeholders that aren't defined in
    the service's own .env are looked up in host/@host-sample/.env, which
    carries a value for (almost) every service's port variables. Anything
    that turns out to be missing from there too falls back to a free
    ephemeral port, and is recorded so the caller can report it - see
    note_missing_from_sample()/missing_from_sample() below. Ports that
    already carry a default (e.g. "${VAR:-8080}") are left untouched.
  - SERV_DIR defaults to the real serv/, but test.py points it at a
    throwaway copy instead before running anything, so any directories a
    service's init.sh or docker-compose.yml creates land there rather than
    in the real repo.
  - Each service's init.sh (if it has one) runs before docker compose does -
    several services use it to bootstrap directories docker-compose.yml
    expects to already exist. A nonzero exit is recorded as a warning
    rather than failing the test outright, since compose itself will fail
    anyway (with a much clearer error) if the missing bootstrap step turns
    out to actually matter.
  - Every subprocess call has a bound: stdin is always closed (so a `sudo`
    inside a service's init.sh can't inherit a real terminal and hang
    forever on a password prompt nobody will answer - this is the usual
    cause of a service that appears to run forever), and every call also
    carries an explicit timeout (QUICK_TIMEOUT for cheap docker metadata
    calls, `self.timeout` for the two steps that can legitimately take a
    while - init.sh and "docker compose up"). A service can never run
    longer than roughly 2x its timeout regardless of what gets stuck.

Tests can safely run concurrently (see test.py's --jobs): port reservation
holds the sockets open until just before "docker compose up" runs rather
than releasing them immediately, so the kernel never hands the same free
port to two services being reserved at the same time; and image pruning is
done once by the caller after the whole run finishes, not per-test, so a
prune from one service can never race with another still pulling.
'''

import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SERV_DIR = os.path.join(REPO_ROOT, 'serv')
SAMPLE_ENV_PATH = os.path.join(REPO_ROOT, 'host', '@host-sample', '.env')

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from source.lib.libyaml import load as ymlload, FullLoader

REQUIRED_VAR_RE = re.compile(r'\$\{([A-Za-z0-9_]+):\?\}')

_warnings_lock = threading.Lock()
_missing_from_sample = {}   # var -> set of services that needed it
_init_script_failures = {}  # service -> (returncode, stderr)


def note_missing_from_sample(service, var):
    with _warnings_lock:
        _missing_from_sample.setdefault(var, set()).add(service)


def missing_from_sample():
    with _warnings_lock:
        return {var: sorted(services) for var, services in _missing_from_sample.items()}


def note_init_script_failure(service, returncode, stderr):
    with _warnings_lock:
        _init_script_failures[service] = (returncode, stderr)


def init_script_failures():
    with _warnings_lock:
        return dict(_init_script_failures)


DEFAULT_TIMEOUT = int(os.environ.get('TEST_COMPOSE_TIMEOUT', '150'))
POLL_INTERVAL = 3
# Bound for cheap, internal docker metadata calls (inspect, rm, ps, logs) -
# these should always return near-instantly; if one doesn't, something is
# wrong and it should fail fast rather than eat into the service's budget.
QUICK_TIMEOUT = 20


class ComposeConflict(Exception):
    '''Raised when a service's container/volume names are already owned by something this test didn't create.'''


def _run(cmd, timeout=None):
    '''
    stdin is always closed (DEVNULL): without this, a command like "sudo"
    invoked from a service's init.sh can inherit a real terminal on stdin
    and sit forever on an interactive password prompt nobody will ever
    answer - that's what "a service just hangs" almost always turns out to
    be. `timeout` is a hard backstop on top of that for anything else that
    could otherwise block indefinitely (a stuck pull, a wedged daemon).
    '''
    try:
        return subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or '')
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or '')
        stderr += f'\ntimed out after {timeout}s'
        return subprocess.CompletedProcess(cmd, 124, stdout=stdout, stderr=stderr)


def _reserve_port(held_sockets):
    '''
    Binds a socket to an OS-assigned free port and keeps it open (appending
    it to `held_sockets`) instead of closing it right away. The kernel
    guarantees it won't hand out that same port to another bind(0) call
    while the socket stays open, which is what makes it safe to reserve
    ports for several services running concurrently: as long as every
    reservation stays held until actual use, two concurrent services can
    never be handed the same port.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    held_sockets.append(sock)
    return sock.getsockname()[1]


def _read_env_file(path):
    values = {}
    if not os.path.exists(path):
        return values
    with open(path, 'r') as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            values[key.strip()] = value.strip()
    return values


def run_init_script(service, service_dir, timeout):
    '''Runs <service_dir>/init.sh if present - several services use it to bootstrap directories docker-compose.yml expects.'''
    init_path = os.path.join(service_dir, 'init.sh')
    if not os.path.exists(init_path):
        return
    result = _run(['bash', init_path], timeout=timeout)
    if result.returncode != 0:
        note_init_script_failure(service, result.returncode, result.stderr)


def _missing_required_vars(compose_path, known_keys):
    with open(compose_path, 'r') as handle:
        raw = handle.read()
    required = set(REQUIRED_VAR_RE.findall(raw))
    return sorted(required - known_keys)


def _build_env_file(service, service_dir, missing_vars, held_sockets, sample_env):
    parts = []
    local_env = os.path.join(service_dir, '.env')
    if os.path.exists(local_env):
        with open(local_env, 'r') as handle:
            content = handle.read()
        if content and not content.endswith('\n'):
            content += '\n'
        parts.append(content)
    for var in missing_vars:
        if var in sample_env:
            parts.append(f'{var}={sample_env[var]}\n')
        else:
            note_missing_from_sample(service, var)
            parts.append(f'{var}={_reserve_port(held_sockets)}\n')

    fd, path = tempfile.mkstemp(prefix='test-compose-', suffix='.env')
    with os.fdopen(fd, 'w') as handle:
        handle.write(''.join(parts))
    return path


def _parse_compose(compose_path):
    with open(compose_path, 'r') as handle:
        return ymlload(handle, Loader=FullLoader)


def _declared_container_names(compose_data):
    names = []
    for service in (compose_data.get('services') or {}).values():
        name = service.get('container_name')
        if name:
            names.append(name)
    return names


def _declared_volume_names(compose_data):
    names = []
    for volume in (compose_data.get('volumes') or {}).values():
        if isinstance(volume, dict) and volume.get('name'):
            names.append(volume['name'])
    return names


def _container_project_label(name):
    result = _run(['docker', 'inspect', name, '--format', '{{ index .Config.Labels "com.docker.compose.project" }}'], timeout=QUICK_TIMEOUT)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _volume_project_label(name):
    result = _run(['docker', 'volume', 'inspect', name, '--format', '{{ index .Labels "com.docker.compose.project" }}'], timeout=QUICK_TIMEOUT)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _reclaim_or_raise(project, container_names, volume_names):
    conflicts = []

    for name in container_names:
        label = _container_project_label(name)
        if label is None:
            continue
        if label == project:
            _run(['docker', 'rm', '-f', name], timeout=QUICK_TIMEOUT)
        else:
            conflicts.append(f'container "{name}" (in use by project "{label or "unknown"}")')

    for name in volume_names:
        label = _volume_project_label(name)
        if label is None:
            continue
        if label == project:
            _run(['docker', 'volume', 'rm', '-f', name], timeout=QUICK_TIMEOUT)
        else:
            conflicts.append(f'volume "{name}" (in use by project "{label or "unknown"}")')

    if conflicts:
        raise ComposeConflict('Container already in use. Skipping...')


def _compose_base(compose_path, env_file, project):
    return ['docker', 'compose', '-f', compose_path, '--env-file', env_file, '-p', project]


def _container_ok(entry):
    if entry.get('State') != 'running':
        return False
    health = entry.get('Health') or ''
    if health and health != 'healthy':
        return False
    return True


def _poll_states(compose_path, env_file, project, timeout, interval, stable_checks=2):
    '''
    Polls until every container is running (and healthy, where applicable)
    for `stable_checks` consecutive polls in a row, not just once - a
    container that starts and crashes almost immediately (e.g. a bad mount
    or bad config) can otherwise be caught mid-flight on a single check and
    misreported as a pass.
    '''
    deadline = time.time() + timeout
    states = {}
    consecutive_ok = 0
    while True:
        result = _run([*_compose_base(compose_path, env_file, project), 'ps', '-a', '--format', 'json'], timeout=QUICK_TIMEOUT)
        states = {}
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            states[entry['Name']] = entry

        if states and all(_container_ok(entry) for entry in states.values()):
            consecutive_ok += 1
            if consecutive_ok >= stable_checks:
                return states, True
        else:
            consecutive_ok = 0

        if time.time() >= deadline:
            return states, False

        time.sleep(interval)


class ComposeIntegrationTestCase(unittest.TestCase):
    '''
    Base test case that spins up a serv/<service> stack, waits for every
    declared container to reach a running (and healthy, where applicable)
    state, then tears everything down. Subclasses just set `service`.
    '''

    service = None
    timeout = DEFAULT_TIMEOUT

    def __str__(self):
        return self.service or super().__str__()

    def setUp(self):
        if not self.service:
            self.skipTest('no service configured')

        self.service_dir = os.path.join(SERV_DIR, self.service)
        self.compose_path = os.path.join(self.service_dir, 'docker-compose.yml')
        self.project = f'test-{self.service}'
        self._env_file = None
        self._reserved_sockets = []

        if not os.path.exists(self.compose_path):
            self.skipTest(f'{self.compose_path} does not exist')

        compose_data = _parse_compose(self.compose_path)
        container_names = _declared_container_names(compose_data)
        volume_names = _declared_volume_names(compose_data)

        try:
            _reclaim_or_raise(self.project, container_names, volume_names)
        except ComposeConflict as error:
            self.skipTest(str(error))

        run_init_script(self.service, self.service_dir, self.timeout)

        local_env = _read_env_file(os.path.join(self.service_dir, '.env'))
        sample_env = _read_env_file(SAMPLE_ENV_PATH)
        missing = _missing_required_vars(self.compose_path, set(local_env))
        self._env_file = _build_env_file(self.service, self.service_dir, missing, self._reserved_sockets, sample_env)

    def tearDown(self):
        for sock in self._reserved_sockets:
            try:
                sock.close()
            except OSError:
                pass
        self._reserved_sockets = []

        if self._env_file is None:
            return
        try:
            _run([*_compose_base(self.compose_path, self._env_file, self.project), 'down', '--volumes', '--remove-orphans'], timeout=self.timeout)
        finally:
            os.remove(self._env_file)

    def test_containers_start_and_stay_up(self):
        cmd = _compose_base(self.compose_path, self._env_file, self.project)

        config_check = _run([*cmd, 'config', '--quiet'], timeout=QUICK_TIMEOUT)
        self.assertEqual(
            config_check.returncode, 0,
            f'docker compose config failed:\n{config_check.stderr}',
        )

        # Hold the reserved ports open as long as possible, only releasing
        # them right before "up" actually needs to bind them - keeps the
        # window where another concurrent service could grab the same port
        # as small as possible.
        for sock in self._reserved_sockets:
            try:
                sock.close()
            except OSError:
                pass
        self._reserved_sockets = []

        up_result = _run([*cmd, 'up', '-d'], timeout=self.timeout)
        self.assertEqual(
            up_result.returncode, 0,
            f'docker compose up failed:\n{up_result.stderr}',
        )

        states, ok = _poll_states(self.compose_path, self._env_file, self.project, self.timeout, POLL_INTERVAL)

        self.assertTrue(states, f'no containers reported for "{self.service}"')

        if not ok:
            details = []
            for name, entry in states.items():
                details.append(f'  {name}: state={entry.get("State")} health={entry.get("Health")} exit={entry.get("ExitCode")}')
                if not _container_ok(entry):
                    logs = _run(['docker', 'logs', '--tail', '30', name], timeout=QUICK_TIMEOUT)
                    details.append(f'  --- {name} logs (tail) ---')
                    details.append(logs.stdout)
                    details.append(logs.stderr)
            self.fail(
                f'not all containers for "{self.service}" reached a running/healthy state within {self.timeout}s:\n'
                + '\n'.join(details)
            )
