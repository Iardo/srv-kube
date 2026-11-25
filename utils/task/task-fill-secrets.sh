#!/bin/bash
set -e
set -o pipefail

# Fills in empty secret values left by "source/secret.py" with real ones,
# generated on this host and never committed to git.
#
# Only touches lines that are still empty, so it's safe to run on every
# deploy: once a value is filled it's left alone. To rotate one by hand,
# blank it out in ".env-secrets.local" and redeploy.
#
# Usage:
#   task-fill-secrets.sh <path-to-.env-secrets.local>

file="$1"

if [ ! -f "$file" ]; then
  exit 0
fi

generate() {
  case "$1" in
    hex32) openssl rand -hex 32 ;;
    hex16) openssl rand -hex 16 ;;
    base64-32) echo "base64:$(openssl rand -base64 32)" ;;
    *) echo "task-fill-secrets.sh: unknown spec '$1'" >&2; exit 1 ;;
  esac
}

changed=0
tmp=$(mktemp)

while IFS= read -r line || [ -n "$line" ]; do
  if [[ "$line" =~ ^([A-Z0-9_]+)=[[:space:]]*#[[:space:]]*generate:[[:space:]]*([a-z0-9-]+)[[:space:]]*$ ]]; then
    name="${BASH_REMATCH[1]}"
    spec="${BASH_REMATCH[2]}"
    value=$(generate "$spec")
    echo "${name}=${value}" >> "$tmp"
    changed=1
  else
    echo "$line" >> "$tmp"
  fi
done < "$file"

if [ "$changed" = "1" ]; then
  mv "$tmp" "$file"
else
  rm -f "$tmp"
fi
