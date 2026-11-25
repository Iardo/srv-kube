#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  mkdir -p $fullpath/../data/database/master
  mkdir -p $fullpath/../data/database/node
fi

if [ ! -d $fullpath/../logs ]; then
  mkdir -p $fullpath/../logs/database/master
  mkdir -p $fullpath/../logs/database/node
fi
