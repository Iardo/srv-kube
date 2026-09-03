#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../data ]; then
  echo "Creating: /data/ssh ..."
  mkdir -p $fullpath/../data/ssh
  echo "Creating: /data/applications ..."
  mkdir -p $fullpath/../data/applications
  echo "Creating: /data/databases ..."
  mkdir -p $fullpath/../data/databases
  echo "Creating: /data/services ..."
  mkdir -p $fullpath/../data/services
  echo "Creating: /data/backups ..."
  mkdir -p $fullpath/../data/backups
  echo "Creating: /data/images ..."
  mkdir -p $fullpath/../data/images
fi
