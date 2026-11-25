#!/usr/bin/env python3

# Ruleset
# --------------------
# Reads "data/models.yml" (symlinked from the host's own data folder)
# and downloads any listed model that isn't already present into "data/models".

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from source.lib.libyaml import load as ymlload, FullLoader

fullpath = os.path.dirname(os.path.abspath(__file__))
conf_path = os.path.join(fullpath, 'data', 'models.yml')
models_path = os.path.join(fullpath, 'data', 'models')

'''
Downloads a single model into "data/models", skipping it if already present.
'''
def download(name: str, url: str):
    dest = os.path.join(models_path, name)
    if os.path.exists(dest):
        print(f'{name} already exists, skipping.')
        return

    print(f'Downloading {name} ...')
    subprocess.run(['curl', '-L', '-C', '-', '-o', dest, '--progress-bar', url], check=True)

def main():
    if not os.path.exists(conf_path):
        print(f'{conf_path} not found, nothing to do.')
        return

    handle = open(conf_path, 'r')
    conf = ymlload(handle, Loader=FullLoader) or {}
    handle.close()

    os.makedirs(models_path, exist_ok=True)

    for entry in conf.get('models') or []:
        download(entry['name'], entry['url'])

main()
