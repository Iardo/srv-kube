#!/usr/bin/env python3

import os
import subprocess

from source.globals.error import Error
from source.globals.strings import Strings
from source.host import Host
from source.service import Service
from source.struct.args import Args


# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    Error.init()
    Strings.init()

    cmd = None
    args = Args.read()
    host = Host.select(args.host)
    conf = Host.conf_read(host)
    file = os.path.join(host, 'docker-compose.yml')

    # Docker Compose Plugin
    if cmd is None:
        try:
            subprocess.call(['docker', 'compose', 'version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cmd = ['docker', 'compose']
        except FileNotFoundError:
            pass

    # Docker Compose Legacy
    if cmd is None:
        try:
            subprocess.call(['docker-compose', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cmd = ['docker-compose']
        except FileNotFoundError:
            pass

    try:
        subprocess.call([*cmd, '-f', file, 'up', '-d', '--build'])
        Service.post(conf)
    except Exception as error:
        print(error)
    
main()
