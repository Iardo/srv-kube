#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -f $fullpath/../conf/server.yml ]; then
  cp $fullpath/../conf/server.example.yml $fullpath/../conf/server.yml
fi
