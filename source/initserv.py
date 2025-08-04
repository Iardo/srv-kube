#!/usr/bin/env python3

import os
import subprocess

class InitServ:
    '''
    Cleans-up all the ports from the environment file
    '''
    @staticmethod
    def init(serv_list: dict, user_conf: list):
        serv_path = os.path.dirname(__file__)
        serv_path = os.path.join(serv_path, '..', 'serv')
        serv_path = os.path.abspath(serv_path)

        for path, subdirs, files in os.walk(serv_path):
            for subdir in subdirs:
                subdir_path = os.path.join(serv_path, subdir)
                if not subdir in user_conf:
                    continue
                for file in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, 'init.sh')
                    if os.path.exists(file_path):
                        if subdir in serv_list:
                            subprocess.call(["sh", "-c", file_path])
                    break
            break
