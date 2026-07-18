#!/usr/bin/env python3

import os
import subprocess

from source.globals.error import Error
from source.globals.strings import Strings
from source.host import Host
from source.struct.args import Args
from source.struct.compose import Compose


# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    Error.init()
    Strings.init()

    cmd = Compose.get_command()
    args = Args.read()
    host = Host.select(args.host)
    file = os.path.join(host, 'docker-compose.yml')

    try:
        subprocess.call([*cmd, '-f', file, "down"])
    except Exception as error:
        print(error)

main()
