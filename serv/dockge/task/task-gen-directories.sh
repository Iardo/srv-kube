#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data ..."
  mkdir -p $fullpath/../data
fi

if [ ! -d $fullpath/../stacks ]; then
  echo "Creating: /stacks ..."
  mkdir -p $fullpath/../stacks
fi
