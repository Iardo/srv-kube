#!/usr/bin/env python3

# Ruleset
# --------------------
# Reads "data/models.yml" (symlinked from the host's own data folder)
# and downloads any listed model that isn't already present into "code/models/<category>".

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from source.lib.libyaml import load as ymlload, FullLoader

fullpath = os.path.dirname(os.path.abspath(__file__))
conf_path = os.path.join(fullpath, 'data', 'models.yml')
models_path = os.path.join(fullpath, 'code', 'models')

'''
Downloads a single model into its category folder, skipping it if already present.
'''
def download(category: str, name: str, url: str):
    dest_dir = os.path.join(models_path, category)
    dest = os.path.join(dest_dir, name)
    if os.path.exists(dest):
        print(f'{name} already exists, skipping.')
        return

    print(f'Downloading {name} ({category}) ...')
    os.makedirs(dest_dir, exist_ok=True)
    subprocess.run(['curl', '-L', '-C', '-', '-o', dest, '--progress-bar', url], check=True)

def main():
    if not os.path.exists(conf_path):
        print(f'{conf_path} not found, nothing to do.')
        return

    handle = open(conf_path, 'r')
    conf = ymlload(handle, Loader=FullLoader) or {}
    handle.close()

    for category, entries in (conf.get('models') or {}).items():
        for entry in entries or []:
            download(category, entry['name'], entry['url'])

main()
