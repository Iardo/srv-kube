#!/usr/bin/env python3

import os
import sys

# Add parent directory to path
actual_dir = os.path.abspath(__file__)
actual_dir = os.path.dirname(actual_dir)
parent_dir = actual_dir
parent_dir = os.path.join(parent_dir, '..', '..')
sys.path.append(parent_dir)

from source.initenv import InitEnv
from source.initserv import InitServ
from source.servlist import serv_list
from source.userconf import UserConf

# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    conf_path = f'{actual_dir}/docker-compose.yml'
    user_conf = UserConf.read(conf_path)
    InitEnv.clean()
    InitEnv.build(serv_list, user_conf)
    InitServ.init(serv_list, user_conf)

main()
