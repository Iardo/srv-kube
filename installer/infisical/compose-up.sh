#!/bin/bash
set -e
set -o pipefail

if ! [ -f .env ]; then
  cp .env.example .env

  secret=$(openssl enc -aes-128-cbc -iter 10000 -nosalt -P -k secret -md sha1 | awk -F= '$1 == "key" {print $2}')
  sed -i "s/=secret/=$secret/" .env
fi

chmod -R 755 ./*
docker-compose up -d
