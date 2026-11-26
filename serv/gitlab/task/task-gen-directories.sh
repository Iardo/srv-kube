#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

for dir in config logs data; do
  if [ ! -d "$fullpath/../data/$dir" ]; then
    echo "Creating: /data/$dir ..."
    mkdir -p "$fullpath/../data/$dir"
  fi
done
