#!/bin/bash
set -e
set -o pipefail

if ! [ -f .env ]; then
  cp .env.example .env

  secret=$(openssl rand -hex 32)
  sed -i "s/=secret/=$secret/" .env
fi

chmod -R 755 ./*
docker-compose up -d
