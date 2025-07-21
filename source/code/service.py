import datetime
import os
import shutil
import subprocess
import sys

from source.lib.libyml import safe_load as ymlload, dump as ymldump, FullLoader

from source.core.load import *
from source.core.string import *

from source.head.values import *
from source.head.theme import *


class service:
    '''
    '''
    @staticmethod
    def init():
        for file in os.listdir(values.conf_bin):
            file_path = f'{values.conf_bin}/{file}'
            os.chmod(file_path, 0o776)

        if not os.path.exists(values.installed_dir):
            os.mkdir(values.installed_dir)

    '''
    Compares list and sync configurations,
    check for differences and generate a list of options to process

    @returns {dict} operations
    '''
    @staticmethod
    def diff() -> dict:
        list_disable: list = []
        list_enable: list = []
        list_install: list = []
        operations: dict
        processing: list = []

        serv, err = load.yml(values.user_services)
        sync, err = load.yml(values.user_sync)

        serv = serv['services'] or []
        sync = sync['services'] or []

        for index, item in enumerate(serv):
            if sync[item]['enabled'] == False:
                action = 'install'
                processing.append({
                    'service': item,
                    'action': action
                })

        for index, item in enumerate(sync):
            if sync[item]['enabled'] == True and \
               not item in serv:
                action = 'uninstall'
                processing.append({
                    'service': item,
                    'action': action
                })

        for operation in processing:
            acts = operation['action']
            name = operation['service']
            path = f'{values.installed_dir}/{name}'
            match acts:
                case 'install':
                    with open(values.user_sync) as data:
                        config_sync = ymlload(data, Loader=FullLoader)
                        check_is_enabled = config_sync['services'][name]['enabled']
                    if check_is_enabled == True:
                        continue
                    if check_is_enabled == False and \
                        os.path.exists(path):
                        list_enable.append(name)
                        continue
                    list_install.append(name)
                case 'uninstall':
                    list_disable.append(name)

        operations = dict(
            list_install=list_install,
            list_enable=list_enable,
            list_disable=list_disable
        )
        return operations

    '''
    Call operations for the services selected

    @param {dict} operations
    '''
    @staticmethod
    def sync(operations: dict):
        list_install = operations['list_install'] or []
        list_enable = operations['list_enable'] or []
        list_disable = operations['list_disable'] or []

        if list_install:
            print(string.color(text=f'Installing: '))
            for serv in list_install:
                service.install(serv)
            print(f'')

        if list_enable:
            print(string.color(text=f'Enabling: '))
            for serv in list_enable:
                service.enable(serv)
            print(f'')

        if list_disable:
            print(string.color(text=f'Disabling: '))
            for serv in list_disable:
                service.disable(serv)
            print(f'')

    '''
    Updates the sync file on an specific service

    @param {str} name
    '''
    @staticmethod
    def update(name: str, state: bool):
        with open(values.user_sync) as data:
            config_sync = ymlload(data, Loader=FullLoader)
            config_sync['services'][name]['enabled'] = state
            config_sync['services'][name]['sync_date'] = datetime.datetime.now()
        with open(values.user_sync, 'w') as outfile:
            ymldump(config_sync, outfile)

    '''
    Remove all services marked as disabled
    '''
    @staticmethod
    def clean():
        for path, subdirs, files in os.walk(values.installed_dir):
            for subdir in subdirs:
                with open(values.user_sync) as data:
                    name = os.path.basename(subdir)
                    name = name.split(' ', 1)[0]
                    path = f'{values.installed_dir}/{name}'
                    config_sync = ymlload(data, Loader=FullLoader)
                    check_is_enabled = config_sync['services'][name]['enabled']
                    if check_is_enabled == False:
                        shutil.rmtree(path)
                        config_sync['services'][name]['running'] = False
                        config_sync['services'][name]['sync_date'] = None
                with open(values.user_sync, 'w') as outfile:
                    ymldump(config_sync, outfile)
            break

    '''
    @param {str} name
    '''
    @staticmethod
    def install(name: str):
        path_target = f'{values.installed_dir}/{name}'
        dotenv_base = f'{values.installed_dir}/{name}/.env.example'
        dotenv_user = f'{values.installed_dir}/{name}/.env'

        for path, subdirs, files in os.walk(values.installer_dir):
            for subdir in subdirs:
                path_base = os.path.basename(subdir)
                path_source = f'{values.installer_dir}/{subdir}'
                if path_base == name:
                    shutil.copytree(path_source, path_target, dirs_exist_ok=True)
            break

        # Change scripts permissions
        # for path, subdirs, files in os.walk(path_target):
        #     for file in files:
        #         path_full = f'{path_target}/{file}'
        #         if file.endswith(".sh"):
        #             os.chmod(path_full, 0o776)

        if os.path.exists(dotenv_base):
            shutil.copyfile(dotenv_base, dotenv_user)

        if sys.platform == 'darwin':
            target_start = f'{path_target}/start.sh'
            # Add double quotes after argument in sed
            subprocess.call(["sed", "-i", "", "s|sed -i|sed -i \"\"|", target_start])
            # Run bcrypt thru htpasswd
            subprocess.call(["sed", "-i", "", "s|\\$BCRYPT -c|htpasswd -bnBC|", target_start])
            subprocess.call(["sed", "-i", "", "s|\\$CRED_PASS)|\\$CRED_USER \\$CRED_PASS)|", target_start])
            subprocess.call(["sed", "-i", "", "s|CRED_HASH=\"\\$CRED_USER\\:|CRED_HASH=\"|", target_start])
            # Change group owner
            subprocess.call(["sed", "-i", "", "s|\\$USER\\:\\$USER|\\$USER\\:staff|", target_start])

        service.update(name, True)

        print(
            string.color(text=f'  `-', fore=theme.text_accent, bold=True),
            string.color(text=f'{name}', fore=theme.text_accent, bold=True),
        )

    '''
    @param {str} name
    '''
    @staticmethod
    def enable(name: str):
        service.update(name, True)

        print(
            string.color(text=f'  `-', fore=theme.text_accent, bold=True),
            string.color(text=f'{name}', fore=theme.text_accent, bold=True),
        )


    '''
    @param {str} name
    '''
    @staticmethod
    def disable(name: str):
        service.update(name, False)

        print(
            string.color(text=f'  `-', fore=theme.text_accent, bold=True),
            string.color(text=f'{name}', fore=theme.text_accent, bold=True),
        )
