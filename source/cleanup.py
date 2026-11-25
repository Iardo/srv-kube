#!/usr/bin/env python3

# Ruleset
# ----------------------
# Resets a host back to a blank slate:
#   - Wipes generated ports/secrets,
#   - Removes the caddy/dnsmasq generated files
#   - Rewrites the include lists plus "komodo-stk.toml" back to their fresh, service-less form.
# 
# Only touches the selected host, never anything else.

import os

from source.envs import Env
from source.secret import Secret

class Cleanup:
    compose_template = "include: []\n"

    dpl_template = (
        "# NOTE:\n"
        "# Used only by Komodo's own stack deploy (see komodo-stk.toml).\n"
        "include: []\n"
    )

    stk_template = (
        '[[stack]]\n'
        'name = "{name}"\n'
        '\n'
        '[stack.config]\n'
        'server        = "{name}"\n'
        'branch        = "kubernetes"\n'
        'repo          = "iardo/srv-kube"\n'
        'clone_path    = "/etc/srv-kube"\n'
        'run_directory = "/etc/srv-kube"\n'
        '\n'
        'file_paths = [\n'
        '    "host/{dirname}/komodo-dpl.yml",\n'
        ']\n'
        '\n'
        'additional_env_files = [\n'
        '    # HOST\n'
        '    {{ track = true,  path = "host/{dirname}/.env" }},\n'
        '    {{ track = false, path = "host/{dirname}/.env-secrets" }},\n'
        '    {{ track = false, path = "host/{dirname}/.env-secrets.local" }},\n'
        ']\n'
        '\n'
        'pre_deploy.shell_mode = false\n'
        'pre_deploy.command = """\n'
        '    [ -f host/{dirname}/.env-secrets.local ] || cp host/{dirname}/.env-secrets host/{dirname}/.env-secrets.local\n'
        '"""\n'
    )

    '''
    Resets the given host to its initial, service-less state.
    '''
    @staticmethod
    def run(host: str):
        try:
            dirname = os.path.basename(os.path.normpath(host))
            name = dirname.lstrip('@')

            Env.strip_overrides(host)
            Env.clean(host)
            Secret.clean(host)

            for filename in ('caddyfile', 'dnsmasq.conf', 'dnsmasq.sh'):
                filepath = os.path.join(host, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)

            compose_path = os.path.join(host, 'docker-compose.yml')
            if os.path.exists(compose_path):
                compose_file = open(compose_path, 'w')
                compose_file.write(Cleanup.compose_template)
                compose_file.close()

            dpl_path = os.path.join(host, 'komodo-dpl.yml')
            if os.path.exists(dpl_path):
                dpl_file = open(dpl_path, 'w')
                dpl_file.write(Cleanup.dpl_template)
                dpl_file.close()

            stk_path = os.path.join(host, 'komodo-stk.toml')
            if os.path.exists(stk_path):
                stk_file = open(stk_path, 'w')
                stk_file.write(Cleanup.stk_template.format(name=name, dirname=dirname))
                stk_file.close()
        except Exception as err:
            print(err)
