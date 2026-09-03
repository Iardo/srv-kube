#!/bin/bash
set -e
set -o pipefail

# Restarts containers when a bind-mounted file actually changed.
# Docker keeps using the old file until the container restarts,
# a plain "git pull" replacing the file on disk is not enough.
#
# Usage:
#   task-restart-if-changed.sh <file> <hash-file> <container> [container...]

file="$1"
hash="$2"
shift 2

if [ ! -f "$file" ]; then
  exit 0
fi

new=$(sha256sum "$file" | cut -d' ' -f1)
old=$(cat "$hash" 2>/dev/null || echo "")

if [ "$new" = "$old" ]; then
  exit 0
fi

echo "$file changed, restarting: $@"
docker restart "$@" 2>/dev/null || true
echo "$new" > "$hash"
