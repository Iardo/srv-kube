#!/usr/bin/env python3

import os
import sys

from source.caddy import Caddy
from source.dnsmasq import Dnsmasq
from source.envs import Env
from source.globals.error import Error
from source.globals.strings import Strings
from source.host import Host
from source.secret import Secret
from source.serv import Service
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
    conf = Host.conf_read(host, ('docker-compose.yml', 'komodo-dpl.yml'))

    Env.clean(host)
    Env.build(host, conf)
    Secret.clean(host)
    Secret.build(host, conf)
    Caddy.clean(host, conf)
    Caddy.build(host, conf)
    Dnsmasq.clean(host, conf)
    Dnsmasq.build(host, conf)
    Dnsmasq.build_script(host, conf)
    Service.init(conf)

main()
