#!/bin/bash
set -e
set -o pipefail

# Adds any key from the committed ".env-secrets" template
# that's missing from this host's untracked ".env-secrets.local".
# Never touches a key ".env-secrets.local" already has.
#
# Needed because the one-time copy in pre_deploy only runs when
# ".env-secrets.local" doesn't exist yet,
# so a key added later never reaches an already-existing one.
#
# Safe to run every deploy, run before "task-fill-secrets.sh".
#
# Usage:
#   task-sync-secrets.sh <path-to-.env-secrets> <path-to-.env-secrets.local>

template="$1"
local="$2"

if [ ! -f "$template" ] || [ ! -f "$local" ]; then
  exit 0
fi

while IFS= read -r line || [ -n "$line" ]; do
  if [[ "$line" =~ ^([A-Z0-9_]+)= ]]; then
    name="${BASH_REMATCH[1]}"
    if ! grep -qE "^${name}=" "$local"; then
      echo "$line" >> "$local"
    fi
  fi
done < "$template"
