import shutil

from source.core.load import *

from source.head.values import *


# TODO: mover todo el codigo de lectura de archivos de config + update de yaml hacia aqui
class config:
    '''
    '''
    @staticmethod
    def init():
        if not os.path.exists(values.user_env):
            shutil.copy(values.conf_env, values.user_env)

        if not os.path.exists(values.user_services):
            shutil.copy(values.conf_services, values.fullpath)

        if not os.path.exists(values.user_sync):
            shutil.copy(values.conf_sync, values.fullpath)

    '''
    '''
    @staticmethod
    def env():
        file, _ = load.ini(values.user_env)
        return file

    '''
    '''
    @staticmethod
    def manifest():
        file, _ = load.yml(values.conf_manifest)
        return file

    '''
    '''
    @staticmethod
    def services():
        file, _ = load.yml(values.user_services)
        return file

    '''
    '''
    @staticmethod
    def sync():
        file, _ = load.yml(values.user_sync)
        return file
