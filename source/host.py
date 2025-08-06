#!/usr/bin/env python3

import os
import sys

from source.lib.libyaml import load as ymlload, FullLoader
from source.globals.color import Color
from source.globals.error import Error
from source.globals.text import Text


host_dir = os.path.abspath(__file__)
host_dir = os.path.dirname(host_dir)
host_dir = os.path.join(host_dir, '..', 'host')

class Host:
    '''
    Reads user configuration and returns its list of services
    '''
    @staticmethod
    def conf_read(host: str):
        user_file = os.path.join(host_dir, host, 'docker-compose.yml')
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
    
    '''
    Takes care of host selection and returns it
    '''
    @staticmethod
    def select(arg_host: str):
        host_pick = -1
        host_list = None
        host_length = None

        # Checks if argument host was passed
        # Checks if host exist
        # Early return to caller
        if arg_host:
            arg_host = os.path.join(host_dir, arg_host)
            if not os.path.exists(arg_host):
                print(Error.SCRIPT_ARG_HOST_NOT_EXIST)
                print()
                sys.exit()
            return arg_host

        # Prints a list of available hosts
        print(Text.HOST_SELECTION_TITLE)
        for path, subdirs, files in os.walk(host_dir):
            subdirs.sort()
            host_list = subdirs
            host_length = len(subdirs) - 1
            for index, subdir in enumerate(subdirs):
                print(f'{Color.text["bold"]}{Color.fore["bright"]["green"]}{index}.{Color.text["reset"]} {subdir}')
            break

        # Wait for user input
        print()
        while host_pick < 0 or \
              host_pick > host_length:
            try:
                host_pick = input(Text.HOST_SELECTION_TEXT)
                host_pick = int(host_pick)
            except ValueError:
                host_pick = -1
                print(Error.INPUT_NAN)
                print()
            except KeyboardInterrupt:
                print()
                sys.exit()
        
        host_pick = os.path.join(host_dir, host_list[host_pick])
        return host_pick
    