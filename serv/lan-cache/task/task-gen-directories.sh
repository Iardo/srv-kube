#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data/cache ]; then
  echo "Creating: /data/cache ..."
  mkdir -p $fullpath/../data/cache
fi
if [ ! -d $fullpath/../data/logs ]; then
  echo "Creating: /data/logs ..."
  mkdir -p $fullpath/../data/logs
fi
