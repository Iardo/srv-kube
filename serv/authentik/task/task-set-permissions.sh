#!/bin/bash
set -e
set -o pipefail

# authentik-worker is hard-pinned to "user: 1000:1000" in docker-compose.yml
# (its outpost integration requires it), so this has to match that exactly,
# not whichever user happens to run this script (root under Komodo).
fullpath=$(dirname "$0")
sys_user=1000
sys_group=1000

echo "Setting Permissions: /cert ..."
chown -R $sys_user:$sys_group $fullpath/../cert/
echo "Setting Permissions: /data ..."
chown -R $sys_user:$sys_group $fullpath/../data/
