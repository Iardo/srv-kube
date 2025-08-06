#!/usr/bin/env python3

import os
import subprocess

from source.core.args import Args
from source.host import Host


# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    args = Args.read()
    host = Host.select(args.host)
    file = os.path.join(host, 'docker-compose.yml')
    subprocess.call(["docker-compose", '-f', file, "down"])

main()
