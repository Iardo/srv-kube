#!/usr/bin/env python3

import os
import sys

# Add parent directory to path
parent_dir = os.path.abspath(__file__)
parent_dir = os.path.dirname(parent_dir)
parent_dir = os.path.join(parent_dir, '..')
sys.path.append(parent_dir)

from source.libyaml import load as ymlload, FullLoader

class UserConf:
    '''
    Reads user configuration and returns its list of services
    '''
    @staticmethod
    def read(user_file):
        handle = open(user_file, 'r')
        user_conf = ymlload(handle, Loader=FullLoader)
        handle.close()
        user_conf = user_conf['include'] or []

        for index, conf in enumerate(user_conf):
            conf = conf.replace('${SERV:?}', '')
            conf = conf.replace('${FILE:?}', '')
            conf = conf.replace('/', '')
            user_conf[index] = conf
        
        return user_conf
