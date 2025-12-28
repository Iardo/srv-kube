#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data/archives ..."
  mkdir -p $fullpath/../data/archives
fi
