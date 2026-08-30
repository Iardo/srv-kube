#!/usr/bin/env python3

import os
import subprocess


serv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'serv'))
link_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'backup'))

class Backup:
    '''
    Checks a service name is real, "serv/<name>" exists.
    '''
    @staticmethod
    def exists(serv: str):
        return os.path.isdir(os.path.join(serv_dir, serv))

    '''
    Runs every service's "task/data-backup.sh" script.
    A service with no such script is just skipped.
    '''
    @staticmethod
    def run(only: str = None):
        for serv in sorted(os.listdir(serv_dir)):
            if only and serv != only:
                continue

            task = os.path.join(serv_dir, serv, 'task', 'data-backup.sh')
            if not os.path.exists(task):
                continue

            print(f'{serv}: backing up ...')
            subprocess.call(['bash', task])
            Backup.link(serv)

    '''
    Points "data/backup/<service>" to "serv/<service>/data/backup",
    so all services' backups show up in one place at the root.
    Skipped if the service has no backup folder yet, or the link is already there.
    '''
    @staticmethod
    def link(serv: str):
        target = os.path.join(serv_dir, serv, 'data', 'backup')
        link = os.path.join(link_dir, serv)

        if not os.path.isdir(target):
            return
        if os.path.islink(link) or os.path.exists(link):
            return

        os.makedirs(link_dir, exist_ok=True)
        os.symlink(os.path.relpath(target, link_dir), link)

    '''
    Restores one backup file into a service.
    Looks for "task/data-restore.sh" first,
    falls back to "task/data-import.sh" if that one doesn't exist.
    What "archive" should look like depends on that script,
    most want the full path to the backup file,
    a few ask for the filename themselves once they start.
    '''
    @staticmethod
    def restore(serv: str, archive: str):
        task = os.path.join(serv_dir, serv, 'task', 'data-restore.sh')
        if not os.path.exists(task):
            task = os.path.join(serv_dir, serv, 'task', 'data-import.sh')
        if not os.path.exists(task):
            print(f'{serv}: no restore script found')
            return

        archive = Backup.find_archive(serv, archive)

        print(f'{serv}: restoring ...')
        subprocess.call(['bash', task, archive])

    '''
    Just a filename, like "2026.01.01-00.00.00-data.tar.gz",
    is looked up inside the service's own "data/backup" folder.
    A path that already points to a real file is left as it is.
    '''
    @staticmethod
    def find_archive(serv: str, archive: str):
        if os.path.isfile(archive):
            return os.path.abspath(archive)

        candidate = os.path.join(serv_dir, serv, 'data', 'backup', archive)
        if os.path.isfile(candidate):
            return candidate

        return archive

    '''
    Finds the newest backup file for a service.
    Restore logs (files ending in "-restore.txt") are skipped,
    they live in the same folder but aren't backups.
    Returns None if the service has no backup file yet.
    '''
    @staticmethod
    def latest_archive(serv: str):
        folder = os.path.join(serv_dir, serv, 'data', 'backup')
        if not os.path.isdir(folder):
            return None

        files = []
        for name in os.listdir(folder):
            if name.endswith('-restore.txt'):
                continue
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                files.append(path)

        if not files:
            return None

        return max(files, key=os.path.getmtime)
