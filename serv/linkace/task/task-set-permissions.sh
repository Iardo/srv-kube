#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath/../")
sys_name=$(uname -s)
sys_user=$USER
sys_group=$USER

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

if [[ "$sys_name" == "Darwin" ]]; then
    sys_group=staff
fi

echo "Setting Permissions: /data ..."
$SUDO chown -R $sys_user:$sys_group $rootpath/data/
