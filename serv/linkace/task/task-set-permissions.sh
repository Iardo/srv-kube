#!/bin/bash
set -e
set -o pipefail

# The container runs as "www-data" (uid 82) baked into the image,
# so this has to match that exactly,
# not whichever user happens to run this script (root under Komodo).
# 
# The ".env" itself is bind-mounted too, LinkAce's own setup
# wizard writes straight into it (e.g. the generated APP_KEY).
fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath/../")
sys_user=82
sys_group=82

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

echo "Setting Permissions: /data ..."
$SUDO chown -R $sys_user:$sys_group $rootpath/data/
echo "Setting Permissions: .env ..."
$SUDO chown $sys_user:$sys_group $rootpath/.env
