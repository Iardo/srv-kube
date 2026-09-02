#!/usr/bin/env python3

import os
import subprocess

'''
Generates a random 32-byte hex secret.
'''
def random_hex():
    result = subprocess.run(['openssl', 'rand', '-hex', '32'], capture_output=True, text=True, check=True)
    return result.stdout.strip()

class Service:
    serv_list: dict = {
        'actual': ['web-http'],
        'adguard-home': ['web-http', 'panel', 'dns-tcp', 'dns-udp'],
        'aria2-pro': ['web-http', 'rpc', 'muse-tcp', 'muse-udp'],
        'authentik': ['web-http', 'web-https', 'database', 'cache'],
        'azimutt': ['web-http', 'database', 'gateway'],
        'bazarr': ['web-http'],
        'caddy': ['web-http', 'web-https', 'web-ui-http', 'web-ui-api'],
        'changedetection': ['web-http'],
        'cloudbeaver': ['web-http'],
        'comfyui': ['web-http'],
        'crafty': ['web-http', 'web-https', 'dynmap', 'bedrock'],
        'cronicle': ['web-http'],
        'cronjob-org': ['web-http', 'database-master', 'database-node'],
        'dnsmasq': ['dns'],
        'dockermon': ['web-http', 'api', 'websocket'],
        'docmost': ['web-http', 'database', 'cache'],
        'docuseal': ['web-http'],
        'dozzle': ['web-http'],
        'drawdb': ['web-http'],
        'epicstore-claimer': ['server'],
        'excalidraw': ['web-http'],
        'firefly3': ['web-http', 'database'],
        'flood': ['web-http'],
        'gatus': ['web-http'],
        'grimoire': ['web-http', 'database'],
        'grist': ['web-http', 'database', 'cache'],
        'guacamole': ['web-http'],
        'highlight': ['web-http'],
        'home-assistant': ['web-http'],
        'homepage': ['web-http'],
        'huly': ['web-http', 'database', 'account', 'collaborator', 'transactor', 'rekoni', 'minio', 'elasticsearch'],
        'immich': ['web-http'],
        'infisical': ['web-http', 'database', 'cache'],
        'jackett': ['web-http'],
        'jellyfin': ['web-http', 'web-https', 'discovery', 'dlna'],
        'kavitareader': ['web-http'],
        'komodo': ['web-http', 'web-https', 'database', 'ferretdb'],
        'linkace': ['web-http', 'web-https', 'database', 'cache'],
        'linkwarden': ['web-http', 'database'],
        'llama-cpp': ['web-http'],
        'mealie': ['web-http'],
        'mirotalksfu': ['web-http'],
        'monica': ['web-http'],
        'n8n': ['web-http', 'database'],
        'netbootxyz': ['web-http', 'assets-http', 'tftp'],
        'netdata': ['web-http'],
        'nginx-proxy-manager': ['web-http', 'web-https', 'panel'],
        'nginx': ['web-http'],
        'notesnook': ['server', 'identity', 'events', 'monograph', 'minio-api', 'minio-web', 'database'],
        'ntfy': ['web-http'],
        'oneuptime': ['web-http'],
        'open-project': ['web-http', 'database'],
        'openhands': ['web-http'],
        'openwebui': ['web-http'],
        'outline': ['web-http', 'web-https', 'database', 'cache'],
        'paperless-ngx': ['web-http', 'database'],
        'passbolt': ['web-http', 'web-https', 'database'],
        'penpot': ['web-http', 'database', 'cache', 'mailcatch'],
        'pihole': ['web-http', 'dns-tcp', 'dns-udp', 'dhcp'],
        'plane': ['web-http', 'database', 'cache', 'minio'],
        'planka': ['web-http', 'database'],
        'portainer': ['web-http'],
        'postal': ['web-http', 'database'],
        'radarr': ['web-http'],
        'romm': ['web-http'],
        'scrutiny': ['web-http', 'database'],
        'sentry': ['web-http'],
        'sonarr': ['web-http'],
        'speedtest-tracker': ['web-http'],
        'stumpapp': ['web-http'],
        'timetagger': ['web-http'],
        'tldraw': ['web-http'],
        'traefik': ['web-http', 'web-https', 'panel'],
        'transmission': ['web-http', 'peer-tcp', 'peer-udp'],
        'trilium-next': ['web-http'],
        'trudesk': ['web-http', 'database', 'elasticsearch', 'elasticsearch-transport'],
        'tuleap': ['web-http'],
        'uptime-kuma': ['web-http'],
        'webcheck': ['web-http'],
        'wger': ['web-http'],
        'wikijs': ['web-http', 'web-https', 'database'],
        'wireguard': ['vpn'],
        'wireguard-easy': ['vpn', 'web-http'],
        'zeroclaw': ['web-http'],
    }

    '''
    Secret variables each service needs, with dummy values.
    '''
    envs_list: dict = {
        'authentik': [
            ('AUTHENTIK_POSTGRESQL__USER', 'authentik # Dummy'),
            ('AUTHENTIK_POSTGRESQL__PASSWORD', 'authentik # Dummy'),
        ],
        'azimutt': [
            ('AZIMUTT_POSTGRES_USER', 'azimutt # Dummy'),
            ('AZIMUTT_POSTGRES_PASS', 'azimutt # Dummy'),
        ],
        'caddy': [
            ('CADDY_UI_USER', 'admin # Dummy'),
            ('CADDY_UI_PASS', 'admin # Dummy'),
            ('CADDY_UI_JWT_SECRET', random_hex),
        ],
        'cronjob-org': [
            ('CRONJOB_ORG_MYSQL_USER_MASTER', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_MYSQL_PASS_MASTER', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_MYSQL_USER_NODE', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_MYSQL_PASS_NODE', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_SESSION_TOKEN_SECRET', random_hex),
            ('CRONJOB_ORG_EMAIL_VERIFICATION_TOKEN_SECRET', random_hex),
            ('CRONJOB_ORG_LOST_PASSWORD_TOKEN_SECRET', random_hex),
            ('CRONJOB_ORG_ACCOUNT_CONFIRMATION_TOKEN_SECRET', random_hex),
            ('CRONJOB_ORG_VERP_SECRET', random_hex),
            ('CRONJOB_ORG_STATUS_BADGE_TOKEN_SECRET', random_hex),
        ],
        'docmost': [
            ('DOCMOST_APP_SECRET', random_hex),
            ('DOCMOST_POSTGRESQL_USER', 'docmost # Dummy'),
            ('DOCMOST_POSTGRESQL_PASS', 'docmost # Dummy'),
        ],
        'immich': [
            ('IMMICH_POSTGRESQL_USER', 'immich # Dummy'),
            ('IMMICH_POSTGRESQL_PASS', 'immich # Dummy'),
        ],
        'komodo': [
            ('KOMODO_DATABASE_USERNAME', 'admin # Dummy'),
            ('KOMODO_DATABASE_PASSWORD', 'admin # Dummy'),
        ],
        'linkace': [
            ('LINKACE_MYSQL_USER', 'linkace # Dummy'),
            ('LINKACE_MYSQL_PASS', 'linkace # Dummy'),
            ('LINKACE_CACHE_PASS', 'linkace # Dummy'),
        ],
        'linkwarden': [
            ('LINKWARDEN_POSTGRES_USER', 'linkwarden # Dummy'),
            ('LINKWARDEN_POSTGRES_PASS', 'linkwarden # Dummy'),
        ],
        'n8n': [
            ('N8N_POSTGRESQL_USER', 'n8n # Dummy'),
            ('N8N_POSTGRESQL_PASS', 'n8n # Dummy'),
            ('N8N_POSTGRESQL_USER_NON_ROOT', 'n8n # Dummy'),
            ('N8N_POSTGRESQL_PASS_NON_ROOT', 'n8n # Dummy'),
        ],
        'notesnook': [
            ('NOTESNOOK_MINIO_ROOT_USER', 'notesnook # Dummy'),
            ('NOTESNOOK_MINIO_ROOT_PASSWORD', 'notesnook # Dummy'),
        ],
        'open-project': [
            ('OPEN_PROJECT_POSTGRESQL_USER', 'openproject # Dummy'),
            ('OPEN_PROJECT_POSTGRESQL_PASS', 'openproject # Dummy'),
            ('OPEN_PROJECT_SECRET_KEY_BASE', random_hex),
        ],
        'openwebui': [
            ('OPENWEBUI_SECRET_KEY', random_hex),
        ],
        'paperless-ngx': [
            ('PAPERLESS_NGX_POSTGRESQL_USER', 'paperlessngx # Dummy'),
            ('PAPERLESS_NGX_POSTGRESQL_PASS', 'paperlessngx # Dummy'),
            ('PAPERLESS_NGX_SECRET_KEY', random_hex),
        ],
        'planka': [
            ('PLANKA_POSTGRES_USER', 'planka # Dummy'),
            ('PLANKA_POSTGRES_PASS', 'planka # Dummy'),
        ],
        'romm': [
            ('ROMM_MYSQL_USER', 'romm # Dummy'),
            ('ROMM_MYSQL_PASS', 'romm # Dummy'),
            ('ROMM_AUTH_SECRET_KEY', random_hex),
        ],
        'timetagger': [
            ('TIMETAGGER_CREDENTIALS', 'timetagger:$$2a$$08$$oFD7M9lLEcvtXWw4ePpVe.k7/vOYUrxrozNlwJnBCgKGXwiIVXdWS # Dummy'),
        ],
        'wger': [
            ('WGER_POSTGRESQL_USER', 'wger # Dummy'),
            ('WGER_POSTGRESQL_PASS', 'wger # Dummy'),
            ('WGER_SECRET_KEY', random_hex),
        ],
        'wikijs': [
            ('WIKIJS_POSTGRES_USER', 'wikijs # Dummy'),
            ('WIKIJS_POSTGRES_PASS', 'wikijs # Dummy'),
        ],
        'wireguard-easy': [
            ('WIREGUARD_EASY_PASSWORD_HASH', '$$2a$$12$$dGVzdGluZ2R1bW15aGFzaHZhbHVlMTIzNDU2 # Dummy, generate a real one with: docker run ghcr.io/wg-easy/wg-easy wgpw yourpassword'),
        ],
        'zeroclaw': [
            ('ZEROCLAW_OPENROUTER_API_KEY', 'sk-or-v1-changeme # Dummy, replace with a real OpenRouter API key'),
        ],
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
                    file_init = os.path.join(subdir_path, 'init.sh')
                    if os.path.exists(file_init):
                        if subdir in Service.serv_list:
                            subprocess.call(["sh", "-c", file_init])
                    break
            break

    '''
    Executes post install tasks for services
    '''
    @staticmethod
    def post(user_conf: list):
        serv_path = os.path.dirname(__file__)
        serv_path = os.path.join(serv_path, '..', 'serv')
        serv_path = os.path.abspath(serv_path)

        for path, subdirs, files in os.walk(serv_path):
            for subdir in subdirs:
                subdir_path = os.path.join(serv_path, subdir)
                if not subdir in user_conf:
                    continue
                for file in os.listdir(subdir_path):
                    task_chmod = os.path.join(subdir_path, 'task', 'data-set-permissions.sh')
                    if os.path.exists(task_chmod):
                        if subdir in Service.serv_list:
                            subprocess.call(["sh", "-c", task_chmod], stdout=subprocess.DEVNULL)
                    break
            break
    