#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../config ]; then
  echo "Creating: /config ..."
  mkdir -p $fullpath/../config
fi
