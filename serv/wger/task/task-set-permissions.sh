#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath/../")

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

# Wger runs as a fixed uid:gid (1000:1000),
# not configurable via PUID/PGID like linuxserver images,
# so this chowns to that numeric id directly
# instead of the deploying user's own.
echo "Setting Permissions: /data ..."
$SUDO chown -R 1000:1000 $rootpath/data/
