#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../cert ]; then
  mkdir -p $fullpath/../cert
fi
if [ ! -d $fullpath/../data ]; then
  mkdir -p $fullpath/../data
fi
