from importlib import import_module
from types import ModuleType
from typing import Any, Tuple, Union

from source.lib.libyml import load as ymlload, FullLoader
from source.lib.libini import ConfigObj

from source.head.msgs import *


class load:
    '''
    Loads yml configuration file

    @param  filepath     : Path to file .yml/.yaml
    @return loads, error :
    '''
    @staticmethod
    def yml(filepath: str) -> Tuple[Any, Union[Exception, None]]:
        loads = Any
        error = None
        handle = None

        try:
            handle = open(filepath, 'r')
            loads = ymlload(handle, Loader=FullLoader)
            handle.close()
        except Exception as err:
            error = err
        finally:
            return loads, error

    '''
    Loads ini configuration file

    @param  filepath    : Path to file .ini
    @return loads, error :
    '''
    @staticmethod
    def ini(filepath: str) -> Tuple[ConfigObj, Union[str, None]]:
        loads = ConfigObj(filepath)
        error = None

        if loads is None:
            error = msgs.HOST_PKGS_ERROR_PKG_FILE_DO_NOT_EXIST
        return loads, error

    '''
    Dynamically imports a module

    @param  name
    @return loads, error
    '''
    @staticmethod
    def mod(name: str) -> Tuple[ModuleType, Union[Exception, None]]:
        loads: ModuleType = ModuleType(name='')
        error = None

        try:
            loads = import_module(name)
        except Exception as err:
            error = err
        finally:
            return loads, error
