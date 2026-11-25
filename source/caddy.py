#!/usr/bin/env python3

import os

from source.host import Host
from source.serv import Service

class Caddy:
    caddy_line_target = "# Services"
    caddy_line_start = 0
    caddy_line_offset = 2 # Offset to preserve the comments

    caddy_header = (
        "# Reverse Proxy\n"
        "# --------------------\n"
        "# https://caddyserver.com/docs/caddyfile\n"
        "\n"
        "# Not published to the host,\n"
        "# only reachable by other containers on the \"caddy\" network (e.g. caddy-ui-backend).\n"
        "{\n"
        "    admin 0.0.0.0:2019\n"
        "    log {\n"
        "        output file /var/log/caddy/access.log\n"
        "    }\n"
        "}\n"
        "\n"
        "# Services\n"
        "# --------------------\n"
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
    Generates one site block per included service
    that has a "web-http"/"web-https" port.

    Only applies to hosts that include "caddy".
    '''
    @staticmethod
    def build(host: str, user_conf: list):
        if 'caddy' not in user_conf:
            return

        try:
            env = Host.read_env_file(os.path.join(host, '.env'))
            # Set CADDY_DOMAIN in the host's .env (Override section) to use a real
            # public domain instead of the internal host-name-based one below,
            # e.g. "actual.iardoo.com" instead of "actual.iardo-vps-iardoo".
            domain = env.get('CADDY_DOMAIN', os.path.basename(os.path.normpath(host)).lstrip('@'))
            # Caddy runs on a custom port here, not the usual 80.
            # It has no way to know that on its own, so each site address
            # below has to say the port out loud.
            # Skip it and Caddy just assumes port 80, which breaks things.
            #
            # NOTE:
            # This still won't fix caddy-ui's own route links though.
            # Its API only exposes "match.host", never the listener's port,
            # so its links always default to :80 regardless of what's set here.
            caddy_web_http = env.get('CADDY_WEB_HTTP', '80')
            # A host that's alone on its machine (no port clash risk) and has
            # its own real public domain can opt into Caddy's automatic HTTPS
            # (Let's Encrypt) instead, set CADDY_AUTO_HTTPS=true and
            # CADDY_WEB_HTTP=80 / CADDY_WEB_HTTPS=443 in that host's .env.
            auto_https = env.get('CADDY_AUTO_HTTPS', 'false').lower() == 'true'

            routes = []
            for serv_name, serv_containers in Service.serv_list.items():
                if serv_name == 'caddy' or serv_name not in user_conf:
                    continue

                prefix = serv_name.replace('-', '_').upper()

                has_http = 'web-http' in serv_containers
                has_https = 'web-https' in serv_containers

                # HTTPS is the one that gets the bare domain name when a service has
                # both: it's the one actually meant to be used, HTTP alongside it is
                # only a fallback, so that's the one that gets the "-http" suffix
                # instead. A service with only one of the two still gets the bare name.
                if has_http:
                    port = env.get(f'{prefix}_WEB_HTTP')
                    if port:
                        name = f'{serv_name}-http' if has_https else serv_name
                        routes.append((name, f'host.docker.internal:{port}', False))

                if has_https:
                    port = env.get(f'{prefix}_WEB_HTTPS')
                    if port:
                        routes.append((serv_name, f'https://host.docker.internal:{port}', True))

            if not routes:
                return

            caddy_path = os.path.join(host, 'caddyfile')
            caddy_file = open(caddy_path, 'a')

            # Explicit "http://" scheme and this host's real port so Caddy
            # doesn't assume standard ports 80/443 and try to auto-upgrade
            # to HTTPS, unless this host opted into auto HTTPS instead, in
            # which case the bare domain lets Caddy provision its own cert.
            for name, upstream, is_https in routes:
                if auto_https:
                    caddy_file.write(f'{name}.{domain} {{\n')
                else:
                    caddy_file.write(f'http://{name}.{domain}:{caddy_web_http} {{\n')
                if is_https:
                    caddy_file.write(f'    reverse_proxy {upstream} {{\n')
                    caddy_file.write(f'        transport http {{\n')
                    caddy_file.write(f'            tls_insecure_skip_verify\n')
                    caddy_file.write(f'        }}\n')
                    caddy_file.write(f'    }}\n')
                else:
                    caddy_file.write(f'    reverse_proxy {upstream}\n')
                caddy_file.write('}\n\n')
            caddy_file.close()
        except Exception as err:
            print(err)
