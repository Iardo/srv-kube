#!/bin/bash
set -e
set -o pipefail

if ! [ -d data ]; then
  chmod -R 755 ./*
fi

docker-compose up -d
