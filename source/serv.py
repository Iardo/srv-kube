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
        'authentik': [
            ('AUTHENTIK_SECRET_KEY', GENERATE_HEX32),
            ('AUTHENTIK_POSTGRESQL__USER', 'authentik # Do not change'),
            ('AUTHENTIK_POSTGRESQL__PASSWORD', 'authentik # Do not change'),
        ],
        'azimutt': [
            ('AZIMUTT_SECRET_KEY_BASE', GENERATE_HEX32),
            ('AZIMUTT_POSTGRES_USER', 'azimutt # Do not change'),
            ('AZIMUTT_POSTGRES_PASS', 'azimutt # Do not change'),
        ],
        'beszel': [
            ('BESZEL_AGENT_TOKEN', 'changeme # Dummy, "Add System" > Token'),
            ('BESZEL_AGENT_KEY', 'changeme # Dummy, "Add System" > Public Key'),
        ],
        'bugsink': [
            ('BUGSINK_SECRET_KEY', GENERATE_HEX32),
            ('BUGSINK_CREATE_SUPERUSER', 'admin@example.com:admin # Do not change; email:password'),
            ('BUGSINK_POSTGRESQL_USER', 'bugsink # Do not change'),
            ('BUGSINK_POSTGRESQL_PASS', 'bugsink # Do not change'),
        ],
        'caddy': [
            ('CADDY_UI_USER', 'admin # Dummy'),
            ('CADDY_UI_PASS', 'admin # Dummy'),
            ('CADDY_UI_JWT_SECRET', GENERATE_HEX32),
        ],
        'coolify': [
            ('COOLIFY_APP_KEY', GENERATE_BASE64_32),
            ('COOLIFY_POSTGRESQL_USER', 'coolify # Do not change'),
            ('COOLIFY_POSTGRESQL_PASS', 'coolify # Do not change'),
            ('COOLIFY_REDIS_PASS', 'coolify # Dummy'),
            ('COOLIFY_PUSHER_APP_ID', GENERATE_HEX32),
            ('COOLIFY_PUSHER_APP_KEY', GENERATE_HEX32),
            ('COOLIFY_PUSHER_APP_SECRET', GENERATE_HEX32),
            ('COOLIFY_ROOT_USERNAME', 'admin # Dummy'),
            ('COOLIFY_ROOT_USER_EMAIL', 'admin@example.com # Dummy'),
            ('COOLIFY_ROOT_USER_PASSWORD', 'coolify # Dummy'),
        ],
        'cronjob-org': [
            ('CRONJOB_ORG_MYSQL_USER_MASTER', 'cronjoborg # Do not change'),
            ('CRONJOB_ORG_MYSQL_PASS_MASTER', 'cronjoborg # Do not change'),
            ('CRONJOB_ORG_MYSQL_USER_NODE', 'cronjoborg # Do not change'),
            ('CRONJOB_ORG_MYSQL_PASS_NODE', 'cronjoborg # Do not change'),
            ('CRONJOB_ORG_SESSION_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_EMAIL_VERIFICATION_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_LOST_PASSWORD_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_ACCOUNT_CONFIRMATION_TOKEN_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_VERP_SECRET', GENERATE_HEX32),
            ('CRONJOB_ORG_STATUS_BADGE_TOKEN_SECRET', GENERATE_HEX32),
        ],
        'docmost': [
            ('DOCMOST_APP_SECRET', GENERATE_HEX32),
            ('DOCMOST_POSTGRESQL_USER', 'docmost # Do not change'),
            ('DOCMOST_POSTGRESQL_PASS', 'docmost # Do not change'),
        ],
        'firefly3': [
            ('FIREFLY3_APP_KEY', GENERATE_HEX16),
        ],
        'github-stars-manager': [
            ('GITHUB_STARS_MANAGER_API_SECRET', GENERATE_HEX32),
            ('GITHUB_STARS_MANAGER_ENCRYPTION_KEY', GENERATE_HEX32),
        ],
        'grafana': [
            ('GRAFANA_ADMIN_USER', 'admin # Do not change'),
            ('GRAFANA_ADMIN_PASSWORD', 'admin # Do not change'),
        ],
        'immich': [
            ('IMMICH_POSTGRESQL_USER', 'immich # Do not change'),
            ('IMMICH_POSTGRESQL_PASS', 'immich # Do not change'),
        ],
        'infisical': [
            ('INFISICAL_POSTGRESQL_USER', 'infisical # Do not change'),
            ('INFISICAL_POSTGRESQL_PASS', 'infisical # Do not change'),
            ('INFISICAL_ENCRYPTION_KEY', GENERATE_HEX16),
            ('INFISICAL_AUTH_SECRET', GENERATE_HEX32),
        ],
        'kaneo': [
            ('KANEO_AUTH_SECRET', GENERATE_HEX32),
            ('KANEO_POSTGRESQL_USER', 'kaneo # Do not change'),
            ('KANEO_POSTGRESQL_PASS', 'kaneo # Do not change'),
        ],
        'komodo': [
            ('KOMODO_DATABASE_USERNAME', 'admin # Do not change'),
            ('KOMODO_DATABASE_PASSWORD', 'admin # Do not change'),
        ],
        'linkace': [
            ('LINKACE_APP_KEY', GENERATE_HEX32),
            ('LINKACE_MYSQL_USER', 'linkace # Do not change'),
            ('LINKACE_MYSQL_PASS', 'linkace # Dummy'),
            # Deliberately not a dummy, and not meant to be hand-edited
            ('LINKACE_MYSQL_ROOT_PASS', GENERATE_HEX32),
            ('LINKACE_CACHE_PASS', 'linkace # Dummy'),
        ],
        'linkwarden': [
            ('LINKWARDEN_NEXTAUTH_SECRET', GENERATE_HEX32),
            ('LINKWARDEN_POSTGRES_USER', 'linkwarden # Do not change'),
            ('LINKWARDEN_POSTGRES_PASS', 'linkwarden # Do not change'),
        ],
        'n8n': [
            ('N8N_POSTGRESQL_USER', 'n8n # Do not change'),
            ('N8N_POSTGRESQL_PASS', 'n8n # Do not change'),
            ('N8N_POSTGRESQL_USER_NON_ROOT', 'n8n # Do not change'),
            ('N8N_POSTGRESQL_PASS_NON_ROOT', 'n8n # Do not change'),
        ],
        'notesnook': [
            ('NOTESNOOK_API_SECRET', GENERATE_HEX32),
            ('NOTESNOOK_MINIO_ROOT_USER', 'notesnook # Do not change'),
            ('NOTESNOOK_MINIO_ROOT_PASSWORD', 'notesnook # Do not change'),
        ],
        'open-project': [
            ('OPEN_PROJECT_POSTGRESQL_USER', 'openproject # Do not change'),
            ('OPEN_PROJECT_POSTGRESQL_PASS', 'openproject # Do not change'),
            ('OPEN_PROJECT_SECRET_KEY_BASE', GENERATE_HEX32),
        ],
        'openwebui': [
            ('OPENWEBUI_SECRET_KEY', GENERATE_HEX32),
        ],
        'outline': [
            ('OUTLINE_SECRET_KEY', GENERATE_HEX32),
            ('OUTLINE_UTILS_SECRET', GENERATE_HEX32),
        ],
        'paperless-ngx': [
            ('PAPERLESS_NGX_POSTGRESQL_USER', 'paperlessngx # Do not change'),
            ('PAPERLESS_NGX_POSTGRESQL_PASS', 'paperlessngx # Do not change'),
            ('PAPERLESS_NGX_SECRET_KEY', GENERATE_HEX32),
        ],
        'passbolt': [
            ('PASSBOLT_POSTGRESQL_USER', 'passbolt # Do not change'),
            ('PASSBOLT_POSTGRESQL_PASS', 'passbolt # Do not change'),
            ('PASSBOLT_ADMIN_EMAIL', ' # Fill-in, see serv/passbolt/readme.md'),
            ('PASSBOLT_ADMIN_FIRSTNAME', ' # Fill-in, see serv/passbolt/readme.md'),
            ('PASSBOLT_ADMIN_LASTNAME', ' # Fill-in, see serv/passbolt/readme.md'),
        ],
        'plane': [
            ('PLANE_SECRET_KEY', GENERATE_HEX32),
            ('PLANE_LIVE_SECRET', GENERATE_HEX32),
            ('PLANE_POSTGRESQL_USER', 'plane # Do not change'),
            ('PLANE_POSTGRESQL_PASS', 'plane # Do not change'),
            ('PLANE_MQ_USER', 'plane # Do not change'),
            ('PLANE_MQ_PASS', GENERATE_HEX32),
            ('PLANE_MINIO_ACCESS_KEY', GENERATE_HEX16),
            ('PLANE_MINIO_SECRET_KEY', GENERATE_HEX32),
        ],
        'planka': [
            ('PLANKA_POSTGRES_USER', 'planka # Do not change'),
            ('PLANKA_POSTGRES_PASS', 'planka # Do not change'),
        ],
        'romm': [
            ('ROMM_MYSQL_USER', 'romm # Do not change'),
            ('ROMM_MYSQL_PASS', 'romm # Do not change'),
            ('ROMM_AUTH_SECRET_KEY', GENERATE_HEX32),
        ],
        'silverbullet': [
            ('SILVERBULLET_USER', 'admin:admin # Dummy'),
        ],
        'timetagger': [
            ('TIMETAGGER_CREDENTIALS', 'timetagger:$$2a$$08$$oFD7M9lLEcvtXWw4ePpVe.k7/vOYUrxrozNlwJnBCgKGXwiIVXdWS # Dummy'),
        ],
        'umami': [
            ('UMAMI_POSTGRESQL_USER', 'umami # Do not change'),
            ('UMAMI_POSTGRESQL_PASS', 'umami # Do not change'),
            ('UMAMI_APP_SECRET', GENERATE_HEX32),
            ('UMAMI_TWO_FACTOR_ENCRYPTION_KEY', GENERATE_HEX32),
        ],
        'wger': [
            ('WGER_POSTGRESQL_USER', 'wger # Do not change'),
            ('WGER_POSTGRESQL_PASS', 'wger # Do not change'),
            ('WGER_SECRET_KEY', GENERATE_HEX32),
        ],
        'wikijs': [
            ('WIKIJS_POSTGRES_USER', 'wikijs # Do not change'),
            ('WIKIJS_POSTGRES_PASS', 'wikijs # Do not change'),
        ],
        'wireguard-easy': [
            ('WIREGUARD_EASY_PASSWORD_HASH', '$$2a$$12$$dGVzdGluZ2R1bW15aGFzaHZhbHVlMTIzNDU2 # Dummy, generate a real one with: docker run ghcr.io/wg-easy/wg-easy wgpw yourpassword'),
        ],
        'woodpecker': [
            ('WOODPECKER_GITHUB_CLIENT', 'changeme # Dummy, GitHub OAuth app -> https://github.com/settings/developers'),
            ('WOODPECKER_GITHUB_SECRET', 'changeme # Dummy, GitHub OAuth app -> https://github.com/settings/developers'),
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
    