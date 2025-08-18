#!/usr/bin/env python3

import os
import subprocess

from source.core.args import Args
from source.host import Host
from source.service import Service


# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    args = Args.read()
    host = Host.select(args.host)
    conf = Host.conf_read(host)
    file = os.path.join(host, 'docker-compose.yml')

    subprocess.call(["docker-compose", '-f', file, "up", "-d", "--build"])
    Service.post(conf)

main()
