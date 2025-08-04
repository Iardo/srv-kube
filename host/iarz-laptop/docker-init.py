#!/usr/bin/env python3

import os
import sys

# Add parent directory to path
actual_dir = os.path.abspath(__file__)
actual_dir = os.path.dirname(actual_dir)
parent_dir = actual_dir
parent_dir = os.path.join(parent_dir, '../../source')
sys.path.append(parent_dir)

from initenv import InitEnv
from initserv import InitServ
from servlist import serv_list
from userconf import UserConf

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
