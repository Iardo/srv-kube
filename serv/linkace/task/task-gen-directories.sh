#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data ..."
  mkdir -p $fullpath/../data
  echo "Creating: /data/backup ..."
  mkdir -p $fullpath/../data/backup
fi
