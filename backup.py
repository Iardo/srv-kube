#!/usr/bin/env python3

import argparse
import os
import sys

from source.backup import Backup

# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    parser = argparse.ArgumentParser(description='Runs the "task/data-backup.sh" script for every service, or just one, or restores one backup file back into a service.')
    parser.add_argument("--only", type=str, required=False, help='The name of a single service to back up or restore.')
    parser.add_argument("--restore", type=str, required=False, help='Path to a backup file to restore. Needs --only to say which service it goes into.')
    parser.add_argument("--restore-last", action="store_true", required=False, help='Restores the newest backup file instead of picking one by hand. Needs --only.')
    args = parser.parse_args()

    if args.only and not Backup.exists(args.only):
        print(f'{args.only}: no such service, check serv/ for the right name')
        sys.exit(1)

    if args.restore or args.restore_last:
        if not args.only:
            print('--restore/--restore-last needs --only, to say which service to restore into')
            sys.exit(1)

        archive = args.restore
        if args.restore_last:
            archive = Backup.latest_archive(args.only)
            if not archive:
                print(f'{args.only}: no backup file found')
                sys.exit(1)

        Backup.restore(args.only, archive)
        return

    Backup.run(args.only)

main()
