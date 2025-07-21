#!/usr/bin/env python3

import os
import sys

# Add parent directory to path
parent_dir = os.path.abspath(__file__)
parent_dir = os.path.dirname(parent_dir)
parent_dir = os.path.join(parent_dir, '..')
sys.path.append(parent_dir)

from envgen import EnvGen

serv_list: dict = {
    'actual': ['web-http'],
    'docmost': ['web-http', 'database', 'redis'],
    'nginx-proxy-manager': ['web-http', 'web-https', 'panel'],
    'notesnook': ['server', 'identity', 'events', 'monograph', 'minio', 'database'],
    'portainer': ['web-http'],
    'timetagger': ['web-http'],
}

# Main
# ----------------------
# enables ansi escape characters in terminal
# required for terminals like cmd.exe in windows
os.system("")

def main():
    EnvGen.clean()
    EnvGen.build(serv_list)

main()
