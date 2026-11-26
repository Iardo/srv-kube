#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

for dir in init data/drive data/record; do
  if [ ! -d "$fullpath/../$dir" ]; then
    echo "Creating: /$dir ..."
    mkdir -p "$fullpath/../$dir"
  fi
done
