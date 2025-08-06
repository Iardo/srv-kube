#!/usr/bin/env python3

# Ruleset
# ----------------------
# Reserve 1,000 spaces per letter of the alphabet
# Reserve a maximum of 10 spaces to assign to each service (Ignored for convenience purposes)

# Ranges
# ----------------------
# Here's a representation of ranges
'''
A = 5000→5999
B = 6000→6999
C = 7000→7999
D = 8000→8999
E = 9000→9999
F = 10000→10999
G = 11000→11999
H = 12000→12999
I = 13000→13999
J = 14000→14999
K = 15000→15999
L = 16000→16999
M = 17000→17999
N = 18000→18999
O = 19000→19999
P = 20000→20999
Q = 21000→21999
R = 22000→22999
S = 23000→23999
T = 24000→24999
U = 25000→25999
V = 26000→26999
W = 27000→27999
X = 28000→28999
Y = 29000→29999
Z = 30000→30999
'''

import os

from enum import Enum
from source.service import Service

class Env:
    env_line_target = "# Generated"
    env_line_start = 0
    env_line_offset = 5 # Offset to preserve the comments

    port_list = Enum('group', [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    port_start_at = 4000

    '''
    Cleans-up all the ports from the environment file
    '''
    @staticmethod
    def clean(host):
        global env_line_start

        try:
            env_path = os.path.join(host, '.env')
            env_file = open(env_path, 'r')
            lines = env_file.readlines()
            for index, text in enumerate(lines):
                if Env.env_line_target in text:
                    env_line_start = index
                    break
            env_file.close()

            env_file = open(env_path, 'w')
            env_file.writelines(lines[:env_line_start + Env.env_line_offset])
            env_file.close()
        except Exception as err:
            print(err)

    '''
    Generates ports for all services and write them to the environment file
    '''
    @staticmethod
    def build(host: str, user_conf: list):
        count = None
        group = ""
        passes = 0
        length = len(Service.serv_list)

        try:
            env_path = os.path.join(host, '.env')
            env_file = open(env_path, 'a')
            for index, (serv_name, serv_containers) in enumerate(Service.serv_list.items()):
                passes = passes + 1

                if not serv_name in user_conf:
                    continue
                if group != serv_name[0]:
                    group = serv_name[0]
                    count = (Env.port_list[serv_name[0]].value * 1000) + Env.port_start_at
                    env_file.write(f'# {group}\n')
                    env_file.write(f'# ----\n')
                if not serv_containers:
                    passes = passes + 1
                    continue
                for serv_container in serv_containers:
                    prefix  = serv_name.replace('-', '_')
                    postfix = serv_container.replace('-', '_')
                    setting = [prefix, postfix]
                    setting = "_".join(setting).upper()
                    env_file.write(f'{setting}={count}\n')
                    count = count + 1
                if passes is not length:
                    env_file.write(f'\n')
            env_file.close()
        except Exception as err:
            print(err)
