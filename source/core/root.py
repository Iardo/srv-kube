import os
import sys

from source.head.msgs import *


class root:
    '''
    Check if script is running with elevated priviledges
    otherwise it gracefully exits the application
    '''
    @staticmethod
    def is_root():
        if not os.geteuid() == 0:
            print(msgs.ERROR_NOT_ROOT)
            print()
            sys.exit()
