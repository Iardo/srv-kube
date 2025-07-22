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
    'aria2-pro': ['web-http', 'rpc', 'muse-tcp', 'muse-udp'],
    'authentik': ['web-http', 'web-https', 'database', 'redis'],
    'azimutt': ['web-http', 'database', 'gateway'],
    'cronicle': ['web-http'],
    'changedetection': ['web-http'],
    'cloudbeaver': ['web-http'],
    'crafty': ['web-http', 'web-https', 'dynmap', 'bedrock'],
    'dockermon': ['web-http', 'api', 'websocket'],
    'docmost': ['web-http', 'database', 'redis'],
    'drawdb': ['web-http'],
    'epicstore-claimer': ['server'],
    'excalidraw': ['web-http'],
    'firefly3': ['web-http', 'database'],
    # 'gatus': ['web-http'],
    'grimoire': ['web-http', 'database'],
    'grist': ['web-http', 'database', 'redis'],
    'guacamole': ['web-http'],
    # 'highlight': ['web-http'],
    'home-assistant': ['web-http'],
    'homepage': ['web-http'],
    'huly': ['web-http', 'database', 'account', 'collaborator', 'transactor', 'rekoni', 'minio', 'elasticsearch'],
    'infisical': ['web-http', 'database', 'redis'],
    'jellyfin': ['web-http', 'web-https', 'discovery', 'dlna'],
    'linkwarden': ['web-http'],
    'mirotalksfu': ['web-http'],
    # 'monica': ['web-http'],
    'n8n': ['web-http', 'database'],
    'netdata': ['web-http'],
    'nginx': ['web-http'],
    'nginx-proxy-manager': ['web-http', 'web-https', 'panel'],
    'notesnook': ['server', 'identity', 'events', 'monograph', 'minio', 'database'],
    # 'oneuptime': ['web-http'],
    'open-project': ['web-http', 'database'],
    'outline': ['web-http', 'web-https', 'database', 'redis'],
    'paperless-ngx': ['web-http', 'database'],
    'passbolt': ['web-http', 'web-https', 'database'],
    'penpot': ['web-http', 'database', 'redis', 'mailcatch'],
    'pihole': ['web-http', 'dns-tcp', 'dns-udp', 'dhcp'],
    'plane': ['web-http', 'database', 'redis', 'minio'],
    'planka': ['web-http', 'database'],
    'portainer': ['web-http'],
    'postal': ['web-http', 'database'],
    'scrutiny': ['web-http', 'database'],
    # 'sentry': ['web-http'],
    'speedtest-tracker': ['web-http'],
    'stumpapp': ['web-http'],
    'timetagger': ['web-http'],
    'tldraw': ['web-http'],
    'traefik': ['web-http', 'web-https', 'panel'],
    'trudesk': ['web-http', 'database', 'elasticsearch', 'elasticsearch-transport'],
    'tuleap': ['web-http'],
    'uptime-kuma': ['web-http'],
    'webcheck': ['web-http'],
    'wikijs': ['web-http', 'web-https', 'database'],
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
