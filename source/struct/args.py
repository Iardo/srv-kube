#!/usr/bin/env python3

import argparse
import os
import sys

from source.globals.error import Error
from source.globals.strings import Strings


class Args:
    '''
    Parse command-line arguments and returns them
    '''
    @staticmethod
    def read():
        parser = argparse.ArgumentParser(description=Strings.get('SCRIPT_DESCRIPTION_INIT'))
        parser.add_argument("--host", type=str, required=False, help=Strings.get('SCRIPT_ARG_HELP_HOST'))
        parser.add_argument("--cleanup", action='store_true', required=False, help=Strings.get('SCRIPT_ARG_HELP_CLEANUP'))
        parser.add_argument("--update-env-local", action='store_true', required=False, help=Strings.get('SCRIPT_ARG_HELP_UPDATE_ENV_LOCAL'))
        args = parser.parse_args()

        return args
