#!/usr/bin/env python3

import os

from source.host import Host
from source.service import Service

class Caddy:
    caddy_line_target = "# Services"
    caddy_line_start = 0
    caddy_line_offset = 2 # Offset to preserve the comments

    caddy_header = (
        "# Reverse Proxy\n"
        "# --------------------\n"
        "# https://caddyserver.com/docs/caddyfile\n"
        "\n"
        "localhost {\n"
        "    # Services\n"
        "    # --------------------\n"
    )

    '''
    Cleans-up the generated reverse-proxy routes from the host's "caddyfile".
    Only applies to hosts that include "caddy",
    creates the file from the template header first if it doesn't exist yet.
    '''
    @staticmethod
    def clean(host, user_conf: list):
        global caddy_line_start

        if 'caddy' not in user_conf:
            return

        try:
            caddy_path = os.path.join(host, 'caddyfile')

            found_marker = False
            if os.path.exists(caddy_path):
                caddy_file = open(caddy_path, 'r')
                lines = caddy_file.readlines()
                caddy_file.close()
                for index, text in enumerate(lines):
                    if Caddy.caddy_line_target in text:
                        caddy_line_start = index
                        found_marker = True
                        break

            if not found_marker:
                caddy_file = open(caddy_path, 'w')
                caddy_file.write(Caddy.caddy_header)
                caddy_file.close()
                return

            caddy_file = open(caddy_path, 'w')
            caddy_file.writelines(lines[:caddy_line_start + Caddy.caddy_line_offset])
            caddy_file.close()
        except Exception as err:
            print(err)

    '''
    Generates a reverse-proxy route for every included service that has a "web-http" port.
    Only applies to hosts that include "caddy".
    '''
    @staticmethod
    def build(host: str, user_conf: list):
        if 'caddy' not in user_conf:
            return

        try:
            env = Host.read_env_file(os.path.join(host, '.env'))
            caddy_path = os.path.join(host, 'caddyfile')
            caddy_file = open(caddy_path, 'a')
            for serv_name, serv_containers in Service.serv_list.items():
                if serv_name == 'caddy' or serv_name not in user_conf:
                    continue

                prefix = serv_name.replace('-', '_').upper()

                if 'web-http' in serv_containers:
                    port = env.get(f'{prefix}_WEB_HTTP')
                    if port:
                        caddy_file.write(f'    handle_path /{serv_name}/* {{\n')
                        caddy_file.write(f'        reverse_proxy host.docker.internal:{port}\n')
                        caddy_file.write(f'    }}\n\n')

                if 'web-https' in serv_containers:
                    port = env.get(f'{prefix}_WEB_HTTPS')
                    if port:
                        caddy_file.write(f'    handle_path /{serv_name}-https/* {{\n')
                        caddy_file.write(f'        reverse_proxy https://host.docker.internal:{port} {{\n')
                        caddy_file.write(f'            transport http {{\n')
                        caddy_file.write(f'                tls_insecure_skip_verify\n')
                        caddy_file.write(f'            }}\n')
                        caddy_file.write(f'        }}\n')
                        caddy_file.write(f'    }}\n\n')
            caddy_file.write('}\n')
            caddy_file.close()
        except Exception as err:
            print(err)
