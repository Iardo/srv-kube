import os

fullpath = os.path.realpath(__file__)
fullpath = os.path.dirname(fullpath)
fullpath = os.path.join(fullpath, '../../')
fullpath = os.path.abspath(fullpath)

class values:
    fullpath: str = fullpath

    # Files
    conf_env: str = f'{fullpath}/.env.example'
    conf_manifest: str = f'{fullpath}/source/static/manifest.yml'
    conf_services: str = f'{fullpath}/source/static/service-list.yml'
    conf_sync: str = f'{fullpath}/source/static/service-sync.yml'
    user_env: str = f'{fullpath}/.env'
    user_services: str = f'{fullpath}/service-list.yml'
    user_sync: str = f'{fullpath}/service-sync.yml'

    # Routes
    dev_temp: str = f'{fullpath}/.tmp'
    conf_bin: str = f'{fullpath}/bin'
    installed_dir: str = f'{fullpath}/installed'
    installer_dir: str = f'{fullpath}/installer'
