#!/usr/bin/env python3

import os
import stat

from source.host import Host

class Dnsmasq:
    dnsmasq_line_target = "# Wildcards"
    dnsmasq_line_start = 0
    dnsmasq_line_offset = 2 # Offset to preserve the comments

    dnsmasq_header = (
        "# DNS\n"
        "# --------------------\n"
        "no-resolv\n"
        "no-hosts\n"
        "server=1.1.1.1\n"
        "server=8.8.8.8\n"
        "\n"
        "# Wildcards\n"
        "# --------------------\n"
    )

    '''
    Cleans-up the generated wildcard rule from the host's "dnsmasq.conf".
    Only applies to hosts that include "dnsmasq",
    creates the file from the template header first if it doesn't exist yet.
    '''
    @staticmethod
    def clean(host, user_conf: list):
        global dnsmasq_line_start

        if 'dnsmasq' not in user_conf:
            return

        try:
            dnsmasq_path = os.path.join(host, 'dnsmasq.conf')

            found_marker = False
            if os.path.exists(dnsmasq_path):
                dnsmasq_file = open(dnsmasq_path, 'r')
                lines = dnsmasq_file.readlines()
                dnsmasq_file.close()
                for index, text in enumerate(lines):
                    if Dnsmasq.dnsmasq_line_target in text:
                        dnsmasq_line_start = index
                        found_marker = True
                        break

            if not found_marker:
                dnsmasq_file = open(dnsmasq_path, 'w')
                dnsmasq_file.write(Dnsmasq.dnsmasq_header)
                dnsmasq_file.close()
                return

            dnsmasq_file = open(dnsmasq_path, 'w')
            dnsmasq_file.writelines(lines[:dnsmasq_line_start + Dnsmasq.dnsmasq_line_offset])
            dnsmasq_file.close()
        except Exception as err:
            print(err)

    '''
    Generates this host's own wildcard rule ("<host-name>", "@" stripped so
    "*.<host-name>" resolves to 127.0.0.1) and writes it to the host's
    "dnsmasq.conf". Only applies to hosts that include "dnsmasq".
    '''
    @staticmethod
    def build(host: str, user_conf: list):
        if 'dnsmasq' not in user_conf:
            return

        try:
            domain = os.path.basename(os.path.normpath(host)).lstrip('@')
            dnsmasq_path = os.path.join(host, 'dnsmasq.conf')
            dnsmasq_file = open(dnsmasq_path, 'a')
            dnsmasq_file.write(f'address=/{domain}/127.0.0.1\n')
            dnsmasq_file.close()
        except Exception as err:
            print(err)

    '''
    Generates the host's "dnsmasq.sh".
    Scoped to the host only, one dnsmasq instance only ever knows its own domain.
    Only applies to hosts that include "dnsmasq".
    '''
    @staticmethod
    def build_script(host: str, user_conf: list):
        if 'dnsmasq' not in user_conf:
            return

        try:
            port = Host.read_env_file(os.path.join(host, '.env')).get('DNSMASQ_DNS', '53')
            domains = [os.path.basename(os.path.normpath(host)).lstrip('@')]

            script_path = os.path.join(host, 'dnsmasq.sh')
            script_file = open(script_path, 'w')
            script_file.write('#!/bin/sh\n')
            script_file.write('# Auto generated running init.py,\n')
            script_file.write('# Do not edit by hand, changes get overwritten on the next run.\n')
            script_file.write('#\n')
            script_file.write('# One-time (per machine) setup so every "*.<host-name>" domain\n')
            script_file.write('# below resolves to 127.0.0.1. Needs sudo.\n')
            script_file.write('set -e\n')
            script_file.write('\n')
            script_file.write(f'PORT={port}\n')
            script_file.write(f'DOMAINS="{" ".join(domains)}"\n')
            script_file.write('\n')
            script_file.write('sudo mkdir -p /etc/systemd/resolved.conf.d\n')
            script_file.write(
                'printf \'[Resolve]\\nDNS=127.0.0.1:%s\\nDomains=%s\\n\' "$PORT" '
                '"$(echo "$DOMAINS" | sed \'s/[^ ]*/~&/g\')" \\\n'
            )
            script_file.write('  | sudo tee /etc/systemd/resolved.conf.d/dnsmasq-wildcards.conf\n')
            script_file.write('sudo systemctl restart systemd-resolved\n')
            script_file.close()

            mode = os.stat(script_path).st_mode
            os.chmod(script_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except Exception as err:
            print(err)
