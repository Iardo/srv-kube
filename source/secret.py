#!/usr/bin/env python3

# Ruleset
# ----------------------
# Dummy values are fixed per variable, not randomly generated,
# so the same service always ships with the same recognizable placeholder.
# Real values belong in ".env-secrets.local" instead.

import os
import shutil

from source.serv import Service

class Secret:
    secret_line_target = "# Services"
    secret_line_start = 0
    secret_line_offset = 2 # Offset to preserve the comments

    '''
    Cleans-up all the generated dummy secrets from the environment file
    '''
    @staticmethod
    def clean(host):
        global secret_line_start

        try:
            secret_path = os.path.join(host, '.env-secrets')
            secret_file = open(secret_path, 'r')
            lines = secret_file.readlines()
            for index, text in enumerate(lines):
                if Secret.secret_line_target in text:
                    secret_line_start = index
                    break
            secret_file.close()

            secret_file = open(secret_path, 'w')
            secret_file.writelines(lines[:secret_line_start + Secret.secret_line_offset])
            secret_file.close()
        except Exception as err:
            print(err)

    '''
    Generates dummy secret values for all services and writes them to ".env-secrets"
    '''
    @staticmethod
    def build(host: str, user_conf: list):
        group = ""
        passes = 0
        length = len(Service.envs_list)

        try:
            secret_path = os.path.join(host, '.env-secrets')
            secret_file = open(secret_path, 'a')
            for index, (serv_name, serv_secrets) in enumerate(Service.envs_list.items()):
                passes = passes + 1

                if not serv_name in user_conf:
                    continue
                if group != serv_name[0]:
                    group = serv_name[0]
                    secret_file.write(f'# {group}\n')
                    secret_file.write(f'# ----\n')
                for name, dummy in serv_secrets:
                    if callable(dummy):
                        secret_file.write(f'{name}={dummy()} # Dummy\n')
                    else:
                        secret_file.write(f'{name}={dummy}\n')
                if passes is not length:
                    secret_file.write(f'\n')
            secret_file.close()
        except Exception as err:
            print(err)

    '''
    Overwrites ".env-secrets.local" with the freshly generated ".env-secrets".

    Development only: ".env-secrets.local" is normally meant to stay fixed once it exists,
    so a live/deployed host never has its already-bootstrapped services' secrets pulled out.
    '''
    @staticmethod
    def update_local(host):
        try:
            secret_path = os.path.join(host, '.env-secrets')
            local_path = os.path.join(host, '.env-secrets.local')
            shutil.copyfile(secret_path, local_path)
        except Exception as err:
            print(err)
