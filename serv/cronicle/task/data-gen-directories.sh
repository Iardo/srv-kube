#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if ! [ -d data ]; then
  mkdir -p $fullpath/../data/cronicle
fi
