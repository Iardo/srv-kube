#!/bin/bash
set -e

if ! [ -d source ]; then
  git clone https://github.com/linkwarden/linkwarden source --depth 1
fi

if [ -f .env ]; then
  SECRET=$(openssl rand -hex 32)

  sed -i "s|NEXTAUTH_SECRET=.*|NEXTAUTH_SECRET=$SECRET|" .env
fi

mkdir -p ./backups
mkdir -p ./logs
chown -R $USER:$USER ./backups
chown -R $USER:$USER ./logs

chmod -R 755 ./*

docker compose up -d --build --pull always
