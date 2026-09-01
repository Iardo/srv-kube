#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data/static ..."
  mkdir -p $fullpath/../data/static
  echo "Creating: /data/media ..."
  mkdir -p $fullpath/../data/media
fi
