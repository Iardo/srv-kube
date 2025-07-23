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
    'cloudbeaver': ['web-http'],
    'cronicle': ['web-http'],
    'dockermon': ['web-http', 'api', 'websocket'],
    'docmost': ['web-http', 'database', 'redis'],
    'excalidraw': ['web-http'],
    'home-assistant': ['web-http'],
    'homepage': ['web-http'],
    'infisical': ['web-http', 'database', 'redis'],
    'linkwarden': ['web-http'],
    'monica': ['web-http'],
    'n8n': ['web-http', 'database'],
    'nginx-proxy-manager': ['web-http', 'web-https', 'panel'],
    'notesnook': ['server', 'identity', 'events', 'monograph', 'minio-api', 'minio-web', 'database'],
    'open-project': ['web-http', 'database'],
    'passbolt': ['web-http', 'web-https', 'database'],
    'penpot': ['web-http', 'database', 'redis', 'mailcatch'],
    'portainer': ['web-http'],
    'postal': ['web-http', 'database'],
    'scrutiny': ['web-http', 'database'],
    'speedtest-tracker': ['web-http'],
    'timetagger': ['web-http'],
    'uptime-kuma': ['web-http'],
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
