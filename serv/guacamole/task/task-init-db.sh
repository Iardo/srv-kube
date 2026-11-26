#!/bin/bash
set -e
set -o pipefail

# Generates the Postgres schema init script once, from the exact pinned
# guacamole/guacamole image (so the schema always matches the app version),
# read by "guacamole-database" on its first boot (empty volume) only.
# Safe to run every deploy: a no-op once "init/initdb.sql" exists.

fullpath=$(dirname "$0")
image="guacamole/guacamole@sha256:700b319ba221d6a5685eb531b27758d3fb2830aa383e94c664296d8b7887db9d"

if [ -f "$fullpath/../init/initdb.sql" ]; then
  exit 0
fi

mkdir -p "$fullpath/../init"
docker run --rm "$image" /opt/guacamole/bin/initdb.sh --postgres > "$fullpath/../init/initdb.sql"
