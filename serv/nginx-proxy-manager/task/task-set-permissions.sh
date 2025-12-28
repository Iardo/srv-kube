#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
sys_name=$(uname -s)
sys_user=$USER
sys_group=$USER

if [[ "$sys_name" == "Darwin" ]]; then
    sys_group=staff
fi

echo "Setting Permissions: /cert ..."
sudo chown -R $sys_user:$sys_group $fullpath/../cert/
echo "Setting Permissions: /data ..."
sudo chown -R $sys_user:$sys_group $fullpath/../data/
