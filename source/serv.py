#!/usr/bin/env python3

import os
import subprocess

# A value starting with "GENERATE:" is never generated here: Secret.build()
# writes it out empty, and "utils/task/task-fill-secrets.sh" fills it in on
# the host itself (first deploy), so the real value never gets committed.
GENERATE_HEX32 = 'GENERATE:hex32'
GENERATE_HEX16 = 'GENERATE:hex16'
GENERATE_BASE64_32 = 'GENERATE:base64-32'

class Service:
    serv_list: dict = {
        'actual': ['web-http'],
        'adguard-home': ['web-http', 'panel', 'dns-tcp', 'dns-udp'],
        'aria2-pro': ['web-http', 'rpc', 'muse-tcp', 'muse-udp'],
        'astral': ['web-http'],
        'authentik': ['web-http', 'web-https', 'database', 'cache'],
        'azimutt': ['web-http', 'database', 'gateway'],
        'bazarr': ['web-http'],
        'beszel': ['web-http'],
        'bugsink': ['web-http'],
        'caddy': ['web-http', 'web-https', 'web-ui-http', 'web-ui-api'],
        'changedetection': ['web-http'],
        'cloudbeaver': ['web-http'],
        'comfyui': ['web-http'],
        'coolify': ['web-http', 'realtime', 'realtime-metrics'],
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
        'github-stars-manager': ['web-http'],
        'grafana': ['web-http'],
        'grimoire': ['web-http', 'database'],
        'grist': ['web-http', 'database', 'cache'],
        'guacamole': ['web-http'],
        'highlight': ['web-http'],
        'home-assistant': ['web-http'],
        'homepage': ['web-http'],
        'huly': ['web-http', 'database', 'account', 'collaborator', 'transactor', 'rekoni', 'minio', 'elasticsearch'],
        'immich': ['web-http'],
        'infisical': ['web-http'],
        'jackett': ['web-http'],
        'jellyfin': ['web-http', 'web-https', 'discovery', 'dlna'],
        'kaneo': ['web-http', 'database'],
        'kavitareader': ['web-http'],
        'komodo': ['web-http', 'web-https', 'database', 'ferretdb'],
        'linkace': ['web-http', 'database', 'cache'],
        'linkwarden': ['web-http', 'database'],
        'llama-cpp': ['web-http'],
        'mailpit': ['web-http', 'smtp'],
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
        'outline': ['web-https', 'database', 'cache'],
        'paperless-ngx': ['web-http', 'database'],
        'passbolt': ['web-https'],
        'penpot': ['web-http', 'database', 'cache', 'mailcatch'],
        'pihole': ['web-http', 'dns-tcp', 'dns-udp', 'dhcp'],
        'plane': ['web-http'],
        'planka': ['web-http', 'database'],
        'portainer': ['web-http'],
        'postal': ['web-http', 'database'],
        'radarr': ['web-http'],
        'romm': ['web-http'],
        'scrutiny': ['web-http', 'database'],
        'sentry': ['web-http'],
        'silverbullet': ['web-http'],
        'sonarr': ['web-http'],
        'speedtest-tracker': ['web-http'],
        'stumpapp': ['web-http'],
        'termix': ['web-http'],
        'timetagger': ['web-http'],
        'tldraw': ['web-http'],
        'traefik': ['web-http', 'web-https', 'panel'],
        'transmission': ['web-http', 'peer-tcp', 'peer-udp'],
        'trilium-next': ['web-http'],
        'trudesk': ['web-http', 'database', 'elasticsearch', 'elasticsearch-transport'],
        'tuleap': ['web-http'],
        'umami': ['web-http'],
        'uptime-kuma': ['web-http'],
        'warpgate': ['web-https', 'ssh', 'mysql'],
        'webcheck': ['web-http'],
        'wger': ['web-http'],
        'wikijs': ['web-http', 'web-https', 'database'],
        'wireguard': ['vpn'],
        'wireguard-easy': ['vpn', 'web-http'],
        'woodpecker': ['web-http'],
        'zeroclaw': ['web-http'],
    }

    '''
    Secret variables each service needs, with dummy values.
    '''
    envs_list: dict = {
        'astral': [
            ('ASTRAL_GITHUB_CLIENT_ID', 'changeme # Dummy, create a GitHub OAuth app at https://github.com/settings/developers'),
            ('ASTRAL_GITHUB_CLIENT_SECRET', 'changeme # Dummy, from the same GitHub OAuth app'),
        ],
        'authentik': [
            ('AUTHENTIK_POSTGRESQL__USER', 'authentik # Dummy'),
            ('AUTHENTIK_POSTGRESQL__PASSWORD', 'authentik # Dummy'),
        ],
        'azimutt': [
            ('AZIMUTT_POSTGRES_USER', 'azimutt # Dummy'),
            ('AZIMUTT_POSTGRES_PASS', 'azimutt # Dummy'),
        ],
        'beszel': [
            ('BESZEL_AGENT_TOKEN', 'changeme # Dummy, from the Hub\'s "Add System" dialog (or Settings > Tokens) after it\'s running'),
            ('BESZEL_AGENT_KEY', 'changeme # Dummy, the public key shown in that same dialog'),
        ],
        'bugsink': [
            ('BUGSINK_SECRET_KEY', GENERATE_HEX32),
            ('BUGSINK_CREATE_SUPERUSER', 'admin@example.com:admin # email:password, do not change'),
            ('BUGSINK_POSTGRESQL_USER', 'bugsink # Dummy'),
            ('BUGSINK_POSTGRESQL_PASS', 'bugsink # Dummy'),
        ],
        'caddy': [
            ('CADDY_UI_USER', 'admin # Dummy'),
            ('CADDY_UI_PASS', 'admin # Dummy'),
            ('CADDY_UI_JWT_SECRET', GENERATE_HEX32),
        ],
        'coolify': [
            ('COOLIFY_APP_KEY', GENERATE_BASE64_32),
            ('COOLIFY_POSTGRESQL_USER', 'coolify # Dummy'),
            ('COOLIFY_POSTGRESQL_PASS', 'coolify # Dummy'),
            ('COOLIFY_REDIS_PASS', 'coolify # Dummy'),
            ('COOLIFY_PUSHER_APP_ID', GENERATE_HEX32),
            ('COOLIFY_PUSHER_APP_KEY', GENERATE_HEX32),
            ('COOLIFY_PUSHER_APP_SECRET', GENERATE_HEX32),
            ('COOLIFY_ROOT_USERNAME', 'admin # Dummy'),
            ('COOLIFY_ROOT_USER_EMAIL', 'admin@example.com # Dummy'),
            ('COOLIFY_ROOT_USER_PASSWORD', 'coolify # Dummy'),
        ],
        'cronjob-org': [
            ('CRONJOB_ORG_MYSQL_USER_MASTER', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_MYSQL_PASS_MASTER', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_MYSQL_USER_NODE', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_MYSQL_PASS_NODE', 'cronjoborg # Dummy'),
            ('CRONJOB_ORG_SESSION_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_EMAIL_VERIFICATION_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_LOST_PASSWORD_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_ACCOUNT_CONFIRMATION_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_VERP_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_STATUS_BADGE_TOKEN_SECRET', GENERATE_HEX32),
        ],
        'docmost': [
            ('DOCMOST_APP_SECRET', GENERATE_HEX32),
            ('DOCMOST_POSTGRESQL_USER', 'docmost # Dummy'),
            ('DOCMOST_POSTGRESQL_PASS', 'docmost # Dummy'),
        ],
        'github-stars-manager': [
            ('GITHUB_STARS_MANAGER_API_SECRET', GENERATE_HEX32),
            ('GITHUB_STARS_MANAGER_ENCRYPTION_KEY', GENERATE_HEX32),
        ],
        'grafana': [
            ('GRAFANA_ADMIN_USER', 'admin # Dummy'),
            ('GRAFANA_ADMIN_PASSWORD', 'admin # Dummy'),
        ],
        'immich': [
            ('IMMICH_POSTGRESQL_USER', 'immich # Dummy'),
            ('IMMICH_POSTGRESQL_PASS', 'immich # Dummy'),
        ],
        'infisical': [
            ('INFISICAL_POSTGRESQL_USER', 'infisical # Dummy'),
            ('INFISICAL_POSTGRESQL_PASS', 'infisical # Dummy'),
            ('INFISICAL_ENCRYPTION_KEY', GENERATE_HEX16),
            ('INFISICAL_AUTH_SECRET', GENERATE_HEX32),
        ],
        'kaneo': [
            ('KANEO_AUTH_SECRET', GENERATE_HEX32),
            ('KANEO_POSTGRESQL_USER', 'kaneo # Dummy'),
            ('KANEO_POSTGRESQL_PASS', 'kaneo # Dummy'),
        ],
        'komodo': [
            ('KOMODO_DATABASE_USERNAME', 'admin # Dummy'),
            ('KOMODO_DATABASE_PASSWORD', 'admin # Dummy'),
        ],
        'linkace': [
            ('LINKACE_MYSQL_USER', 'linkace # Do not change'),
            ('LINKACE_MYSQL_PASS', 'linkace # Dummy'),
            # Deliberately not a dummy, and not meant to be hand-edited
            ('LINKACE_MYSQL_ROOT_PASS', GENERATE_HEX32),
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
            ('OPEN_PROJECT_SECRET_KEY_BASE', GENERATE_HEX32),
        ],
        'openwebui': [
            ('OPENWEBUI_SECRET_KEY', GENERATE_HEX32),
        ],
        'paperless-ngx': [
            ('PAPERLESS_NGX_POSTGRESQL_USER', 'paperlessngx # Dummy'),
            ('PAPERLESS_NGX_POSTGRESQL_PASS', 'paperlessngx # Dummy'),
            ('PAPERLESS_NGX_SECRET_KEY', GENERATE_HEX32),
        ],
        'passbolt': [
            ('PASSBOLT_POSTGRESQL_USER', 'passbolt # Dummy'),
            ('PASSBOLT_POSTGRESQL_PASS', 'passbolt # Dummy'),
        ],
        'plane': [
            ('PLANE_SECRET_KEY', GENERATE_HEX32),
            ('PLANE_LIVE_SECRET', GENERATE_HEX32),
            ('PLANE_POSTGRESQL_USER', 'plane # Dummy'),
            ('PLANE_POSTGRESQL_PASS', 'plane # Dummy'),
            ('PLANE_MQ_USER', 'plane # Dummy'),
            ('PLANE_MQ_PASS', GENERATE_HEX32),
            ('PLANE_MINIO_ACCESS_KEY', GENERATE_HEX16),
            ('PLANE_MINIO_SECRET_KEY', GENERATE_HEX32),
        ],
        'planka': [
            ('PLANKA_POSTGRES_USER', 'planka # Dummy'),
            ('PLANKA_POSTGRES_PASS', 'planka # Dummy'),
        ],
        'romm': [
            ('ROMM_MYSQL_USER', 'romm # Dummy'),
            ('ROMM_MYSQL_PASS', 'romm # Dummy'),
            ('ROMM_AUTH_SECRET_KEY', GENERATE_HEX32),
        ],
        'silverbullet': [
            ('SILVERBULLET_USER', 'admin:admin # Dummy'),
        ],
        'timetagger': [
            ('TIMETAGGER_CREDENTIALS', 'timetagger:$$2a$$08$$oFD7M9lLEcvtXWw4ePpVe.k7/vOYUrxrozNlwJnBCgKGXwiIVXdWS # Dummy'),
        ],
        'umami': [
            ('UMAMI_POSTGRESQL_USER', 'umami # Dummy'),
            ('UMAMI_POSTGRESQL_PASS', 'umami # Dummy'),
            ('UMAMI_APP_SECRET', GENERATE_HEX32),
            ('UMAMI_TWO_FACTOR_ENCRYPTION_KEY', GENERATE_HEX32),
        ],
        'wger': [
            ('WGER_POSTGRESQL_USER', 'wger # Dummy'),
            ('WGER_POSTGRESQL_PASS', 'wger # Dummy'),
            ('WGER_SECRET_KEY', GENERATE_HEX32),
        ],
        'wikijs': [
            ('WIKIJS_POSTGRES_USER', 'wikijs # Dummy'),
            ('WIKIJS_POSTGRES_PASS', 'wikijs # Dummy'),
        ],
        'wireguard-easy': [
            ('WIREGUARD_EASY_PASSWORD_HASH', '$$2a$$12$$dGVzdGluZ2R1bW15aGFzaHZhbHVlMTIzNDU2 # Dummy, generate a real one with: docker run ghcr.io/wg-easy/wg-easy wgpw yourpassword'),
        ],
        'woodpecker': [
            ('WOODPECKER_GITHUB_CLIENT', 'changeme # Dummy, create a GitHub OAuth app at https://github.com/settings/developers'),
            ('WOODPECKER_GITHUB_SECRET', 'changeme # Dummy, from the same GitHub OAuth app'),
            ('WOODPECKER_AGENT_SECRET', GENERATE_HEX32),
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
    