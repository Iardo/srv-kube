#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data/consume ..."
  mkdir -p $fullpath/../data/consume
  echo "Creating: /data/export ..."
  mkdir -p $fullpath/../data/export
fi
