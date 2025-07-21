import datetime
import os
import subprocess

from source.lib.libyml import safe_load as ymlload, dump as ymldump, FullLoader

from source.core.load import *
from source.core.string import *

from source.head.values import *
from source.head.theme import *


class container:
    '''
    '''
    @staticmethod
    def diff() -> dict:
        operations: dict
        list_start: list = []
        list_stops: list = []

        for path, subdirs, files in os.walk(values.installed_dir):
            for subdir in subdirs:
                base = os.path.basename(subdir)
                name = base.split(' ', 1)[0]
                with open(values.user_sync) as data:
                    config_sync = ymlload(data, Loader=FullLoader)
                    check_is_enabled = config_sync['services'][name]['enabled']
                    check_is_running = config_sync['services'][name]['running']
                    check_is_process = subprocess.run(
                        ['docker', 'inspect', '-f', '"{{.State.Status}}"', f'{name}'],
                        stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT,
                        universal_newlines = True,
                    )
                    check_is_process = check_is_process.stdout.strip("\n")
                    check_is_process = True if check_is_process == '"running"' else False

                    if check_is_enabled == True and \
                       check_is_running == True:
                        continue

                    if check_is_enabled == False and (check_is_running == True or check_is_process == True):
                        list_stops.append(name)
                        continue

                    if check_is_enabled == True and \
                       check_is_running == False:
                        list_start.append(name)
            break

        operations = dict(
            list_start=list_start,
            list_stops=list_stops
        )
        return operations

    '''
    '''
    @staticmethod
    def sync(operations: dict):
        list_start = operations['list_start'] or []
        list_stops = operations['list_stops'] or []

        if list_start:
            print(string.color(text=f'Starting: '))
            for serv in list_start:
                container.start(serv)
            print(string.color(text=f'{"":-^50}', fore=theme.text_accent, bold=True))
            print(f'')

        if list_stops:
            print(string.color(text=f'Stopping: '))
            for serv in list_stops:
                container.stops(serv)
            print(string.color(text=f'{"":-^50}', fore=theme.text_accent, bold=True))
            print(f'')

    '''
    Updates the sync file on an specific service

    @param {str} name
    '''
    @staticmethod
    def update(name: str, state: bool):
        with open(values.user_sync) as data:
            config_sync = ymlload(data, Loader=FullLoader)
            config_sync['services'][name]['running'] = state
            config_sync['services'][name]['sync_date'] = datetime.datetime.now()
        with open(values.user_sync, 'w') as outfile:
            ymldump(config_sync, outfile)

    '''
    @param {str} name
    '''
    def start(name: str):
        path_target = f'{values.installed_dir}/{name}'

        print(
            string.color(text=f'  `-', fore=theme.text_accent, bold=True),
            string.color(text=f'{name}', fore=theme.text_accent, bold=True),
        )

        if os.path.exists(f'{path_target}/start.sh'):
            try:
                return_code = subprocess.call(['sh', 'start.sh'], cwd=path_target)
                if return_code != 0:
                    return
                container.update(name, True)
            except Exception as err:
                print(err)

    '''
    @param {str} name
    '''
    def stops(name: str):
        path_install = f'{values.installed_dir}/{name}'

        print(
            string.color(text=f'  `-', fore=theme.text_accent, bold=True),
            string.color(text=f'{name}', fore=theme.text_accent, bold=True),
        )
        print(string.color(text=f'{"":-^50}', fore=theme.text_accent, bold=True))

        if os.path.exists(f'{path_install}/stops.sh'):
            path_target = path_install

        try:
            subprocess.call(['sh', 'stops.sh'], cwd=path_target, stdin=subprocess.PIPE)
            container.update(name, False)
        except Exception as err:
            print(err)
