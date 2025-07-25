#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if ! [ -d data ]; then
  echo "Creating: /data/assets ..."
  mkdir -p $fullpath/../data/assets
  echo "Creating: /data/backup ..."
  mkdir -p $fullpath/../data/backup
  echo "Creating: /logs ..."
  mkdir -p $fullpath/../logs
fi
