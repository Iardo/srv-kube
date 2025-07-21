#!/bin/bash
set -e

if [ -f .env ]; then
  SECRET=$(openssl rand -hex 32)

  sed -i "s|SECRET_KEY_BASE=.*|SECRET_KEY_BASE=$SECRET|" .env
fi

chmod -R 755 ./*
docker-compose up -d
