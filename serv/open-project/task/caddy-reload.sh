#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

echo "Reloading: Caddy ..."
quiet docker exec -it open-project-proxy caddy fmt --config /etc/caddy/Caddyfile --overwrite
quiet docker exec -it open-project-proxy caddy reload --config /etc/caddy/Caddyfile
