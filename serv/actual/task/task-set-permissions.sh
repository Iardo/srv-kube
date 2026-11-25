#!/bin/bash
set -e
set -o pipefail

# The container is hard-pinned to this UID/GID in docker-compose.yml
# ("user: ${ACTUAL_UID:-1000}:${ACTUAL_GID:-1000}"), so this has to match that
# exactly, not whichever user happens to run this script (root under Komodo).
fullpath=$(dirname "$0")
sys_user=${ACTUAL_UID:-1000}
sys_group=${ACTUAL_GID:-1000}

chown -R $sys_user:$sys_group $fullpath/../cert/
chown -R $sys_user:$sys_group $fullpath/../data/
