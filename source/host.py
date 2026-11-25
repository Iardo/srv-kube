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
    Reads host configuration and returns its list of services.
    Reads host "docker-compose.yml" and "komodo-dpl.yml".
    '''
    @staticmethod
    def conf_read(host: str, file_names: tuple = ('docker-compose.yml',)):
        services = []

        for file_name in file_names:
            user_file = os.path.join(host_dir, host, file_name)
            if not os.path.exists(user_file):
                continue

            handle = open(user_file, 'r')
            user_conf = ymlload(handle, Loader=FullLoader)
            handle.close()
            user_conf = user_conf['include'] or []

            for conf in user_conf:
                conf = conf.replace('${SERV:?}', '')
                conf = conf.replace('${FILE:?}', '')
                conf = conf.replace('/', '')
                if conf not in services:
                    services.append(conf)

        return services
    
    '''
    Reads one env file into a dict,
    a value can be quoted or have a trailing comment like "# Dummy",
    same as how compose reads its own env files.
    '''
    @staticmethod
    def read_env_file(path: str):
        values = {}

        if not os.path.exists(path):
            return values

        handle = open(path, 'r')
        for line in handle.readlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            value = value.strip()

            if value[:1] in ('"', "'") and value.endswith(value[:1]) and len(value) > 1:
                value = value[1:-1]
            elif ' #' in value:
                value = value.split(' #', 1)[0].strip()

            values[key.strip()] = value
        handle.close()

        return values

    '''
    Reads the host's secret overrides, layering files:
      - ".env-secrets"       : Tracked in git, ships with dummy example values so every variable name is documented and easy to find.
      - ".env-secrets.local" : Gitignored, empty/absent by default. It need to be changed directly on a deployed host, survive future deploys.
    '''
    @staticmethod
    def secrets_read(host: str):
        secrets = Host.read_env_file(os.path.join(host, '.env-secrets'))
        secrets.update(Host.read_env_file(os.path.join(host, '.env-secrets.local')))
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
    