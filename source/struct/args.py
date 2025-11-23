#!/usr/bin/env python3

import argparse
import os
import sys

from source.globals.error import Error
from source.globals.text import Text


class Args:
    '''
    Parse command-line arguments and returns them
    '''
    @staticmethod
    def read():
        parser = argparse.ArgumentParser(description=Text.SCRIPT_DESCRIPTION_INIT)
        parser.add_argument("--host", type=str, required=False, help=Text.SCRIPT_ARG_HELP_HOST)
        args = parser.parse_args()

        return args
