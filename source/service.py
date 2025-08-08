#!/usr/bin/env python3

import os
import subprocess

class Service:
    serv_list: dict = {
        'actual': ['web-http'],
        'aria2-pro': ['web-http', 'rpc', 'muse-tcp', 'muse-udp'],
        'authentik': ['web-http', 'web-https', 'database', 'redis'],
        'azimutt': ['web-http', 'database', 'gateway'],
        'changedetection': ['web-http'],
        'cloudbeaver': ['web-http'],
        'crafty': ['web-http', 'web-https', 'dynmap', 'bedrock'],
        'cronicle': ['web-http'],
        'dockermon': ['web-http', 'api', 'websocket'],
        'docmost': ['web-http', 'database', 'redis'],
        'drawdb': ['web-http'],
        'epicstore-claimer': ['server'],
        'excalidraw': ['web-http'],
        'firefly3': ['web-http', 'database'],
        'gatus': ['web-http'],
        'grimoire': ['web-http', 'database'],
        'grist': ['web-http', 'database', 'redis'],
        'guacamole': ['web-http'],
        'highlight': ['web-http'],
        'home-assistant': ['web-http'],
        'homepage': ['web-http'],
        'huly': ['web-http', 'database', 'account', 'collaborator', 'transactor', 'rekoni', 'minio', 'elasticsearch'],
        'infisical': ['web-http', 'database', 'redis'],
        'jellyfin': ['web-http', 'web-https', 'discovery', 'dlna'],
        'linkwarden': ['web-http', 'database'],
        'mirotalksfu': ['web-http'],
        'monica': ['web-http'],
        'n8n': ['web-http', 'database'],
        'netdata': ['web-http'],
        'nginx-proxy-manager': ['web-http', 'web-https', 'panel'],
        'nginx': ['web-http'],
        'notesnook': ['server', 'identity', 'events', 'monograph', 'minio-api', 'minio-web', 'database'],
        'oneuptime': ['web-http'],
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
        'sentry': ['web-http'],
        'speedtest-tracker': ['web-http'],
        'stumpapp': ['web-http'],
        'timetagger': ['web-http'],
        'tldraw': ['web-http'],
        'traefik': ['web-http', 'web-https', 'panel'],
        'trilium-next': ['web-http'],
        'trudesk': ['web-http', 'database', 'elasticsearch', 'elasticsearch-transport'],
        'tuleap': ['web-http'],
        'uptime-kuma': ['web-http'],
        'webcheck': ['web-http'],
        'wikijs': ['web-http', 'web-https', 'database'],
    }

    '''
    Initializes services with an init.sh file
    '''
    @staticmethod
    def init(user_conf: list):
        serv_path = os.path.dirname(__file__)
        serv_path = os.path.join(serv_path, '..', 'serv')
        serv_path = os.path.abspath(serv_path)

        for path, subdirs, files in os.walk(serv_path):
            for subdir in subdirs:
                subdir_path = os.path.join(serv_path, subdir)
                if not subdir in user_conf:
                    continue
                for file in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, 'init.sh')
                    if os.path.exists(file_path):
                        if subdir in Service.serv_list:
                            subprocess.call(["sh", "-c", file_path])
                    break
            break
