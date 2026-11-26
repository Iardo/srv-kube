#!/bin/bash
set -e
set -o pipefail

# The container's nginx/php-fpm processes run as "nobody" (uid 65534) and
# "www-data"-equivalent group (gid 82), baked into the image, so this has
# to match that exactly, not whichever user happens to run this script
# (root under Komodo).
fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath/../")
sys_user=65534
sys_group=82

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

echo "Setting Permissions: /data ..."
$SUDO chown -R $sys_user:$sys_group $rootpath/data/
