#!/usr/bin/env python3

import os
import sys

from source.environment import Env
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

    args = Args.read()
    host = Host.select(args.host)
    conf = Host.conf_read(host)

    Env.clean(host)
    Env.build(host, conf)
    Service.init(conf)

main()
