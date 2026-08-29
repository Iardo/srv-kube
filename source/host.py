#!/usr/bin/env python3

import os
import sys

from source.lib.libyaml import load as ymlload, FullLoader
from source.globals.color import Color
from source.globals.error import Error
from source.globals.strings import Strings


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
    Reads the host's ".env-secrets" override file
    '''
    @staticmethod
    def secrets_read(host: str):
        secrets = {}
        secrets_path = os.path.join(host, '.env-secrets')

        if not os.path.exists(secrets_path):
            return secrets

        handle = open(secrets_path, 'r')
        for line in handle.readlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            value = value.strip()

            # Quoted values are taken verbatim; unquoted values can carry
            # an inline "# comment" (e.g. "# Dummy"), same as compose's
            # own env file parsing.
            if value[:1] in ('"', "'") and value.endswith(value[:1]) and len(value) > 1:
                value = value[1:-1]
            elif ' #' in value:
                value = value.split(' #', 1)[0].strip()

            secrets[key.strip()] = value
        handle.close()

        return secrets

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
                print(Error.get('SCRIPT_ARG_HOST_NOT_EXIST'))
                print()
                sys.exit()
            return arg_host

        # Prints a list of available hosts
        print(Strings.get('HOST_SELECTION_TITLE'))
        for path, subdirs, files in os.walk(host_dir):
            subdirs.sort()
            host_list = subdirs
            host_length = len(subdirs) - 1
            for index, subdir in enumerate(subdirs):
                print(f'{Color.text["type"]["bold"]}{Color.fore["bright"]["green"]}{index}.{Color.text["type"]["reset"]} {subdir}')
            break

        # Wait for user input
        print()
        while host_pick < 0 or \
              host_pick > host_length:
            try:
                host_pick = input(Strings.get('HOST_SELECTION_TEXT'))
                host_pick = int(host_pick)
            except ValueError:
                host_pick = -1
                print(Error.get('INPUT_NAN'))
                print()
            except KeyboardInterrupt:
                print()
                sys.exit()
        
        host_pick = os.path.join(host_dir, host_list[host_pick])
        return host_pick
    