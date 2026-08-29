#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
sys_name=$(uname -s)
sys_user=${USER:-1000}
sys_group=${USER:-1000}

if [[ "$sys_name" == "Darwin" ]]; then
    sys_group=staff
fi

echo "Setting Permissions: /data ..."
chown -R $sys_user:$sys_group $fullpath/../data/
chown -R $sys_user:$sys_group $fullpath/../logs/
