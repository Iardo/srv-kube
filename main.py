#!/bin/python

import os
import sys

from source.code.backup import *
from source.code.config import *
from source.code.container import *
from source.code.dev import *
from source.code.service import *

from source.core.load import *
from source.core.string import *

from source.head.color import *
from source.head.msgs import *
from source.head.theme import *
from source.head.values import *

    
'''
'''
def selection():
    print(string.color(text=f'Executing: '), end='')

    option = sys.argv[1] if len(sys.argv) > 1 else None
    
    match option:
        case 'sync':
            print(string.color(text='sync', fore=theme.text_accent, bold=True))
            serv_op = service.diff()
            service.sync(serv_op)

            cont_op = container.diff()
            container.sync(cont_op)
        case 'clean':
            print(string.color(text='clean', fore=theme.text_accent, bold=True))
            service.clean()
        case 'backup':
            print(string.color(text='backup', fore=theme.text_accent, bold=True))
            backup.services()
        case 'dev':
            print(string.color(text='development', fore=theme.text_accent, bold=True))
            dev.init()
            dev.restart('')
        case _:
            print(string.color(text='none', fore=theme.text_accent, bold=True))
            print(f'')
            sys.exit()


# Main
# --------------------------------------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    config.init()
    service.init()
    selection()

main()
