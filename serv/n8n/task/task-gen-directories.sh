#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data ..."
  mkdir -p $fullpath/../data
  echo "Creating: /data/backup ..."
  mkdir -p $fullpath/../data/backup
fi

if [ ! -d $fullpath/../logs ]; then
  echo "Creating: /logs ..."
  mkdir -p $fullpath/../logs
  echo "Creating: /logs/backup ..."
  mkdir -p $fullpath/../logs/backup
fi
