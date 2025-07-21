import os
import shutil

from source.code.config import *
from source.code.container import *
from source.code.service import *

from source.core.string import *

from source.head.values import *


class dev:
    '''
    Initialize development mode
    '''
    @staticmethod
    def init():
        env_file = config.env()
        check_dev_mode = string.to_bool(env_file['DEV_MODE'])
        check_dev_temp = os.path.exists(values.dev_temp)

        if check_dev_mode == True and\
           check_dev_temp == False:
            os.mkdir(values.dev_temp)
        
        if check_dev_mode == False and\
           check_dev_temp == True:
            shutil.rmtree(values.dev_temp)

    '''
    Clean-up and re-install service for testing
    
    @param {str} name
    '''
    @staticmethod
    def restart():
        env_file = config.env()
        check_dev_mode = string.to_bool(env_file['DEV_MODE'])

        if check_dev_mode == True:
            # TODO: run stops.sh
            # TODO: remove dir
            # TODO: copy dir again
            # TODO: run start.sh
            pass
