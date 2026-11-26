#!/bin/bash
set -e
set -o pipefail

# The plain (non-"s6") image runs as a baked-in uid/gid 1000, and does not
# honor PUID/PGID (that only works on the separate "s6" image variant, which
# has its own open bugs applying ownership to mounted volumes), so this has
# to match 1000:1000 exactly, not whichever user runs this script (root under
# Komodo).
fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath/../")
sys_user=1000
sys_group=1000

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

echo "Setting Permissions: /data ..."
$SUDO chown -R $sys_user:$sys_group $rootpath/data/
