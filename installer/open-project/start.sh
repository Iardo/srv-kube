#!/bin/bash
set -e

if [ -f .env ]; then
  HTTPS=false
  PORT=0.0.0.0:8080
  HOST=localhost
  HOSTS='["127.0.0.1", "172.0.0.0/8", "192.168.0.0/16"]'
  OPDATA=\"./assets\"

  sed -i "s|PORT=.*|PORT=$PORT|" .env
  sed -i "s|OPENPROJECT_HTTPS=.*|OPENPROJECT_HTTPS=$HTTPS|" .env
  sed -i "s|OPENPROJECT_HOST__NAME=.*|OPENPROJECT_HOST__NAME=$HOST|" .env
  sed -i "s|OPENPROJECT_ADDITIONAL__HOST__NAMES=.*|OPENPROJECT_ADDITIONAL__HOST__NAMES=$HOSTS|" .env
  sed -i "s|OPDATA=.*|OPDATA=$OPDATA|" .env
fi

if [ -f caddyfile.template ]; then
  HOST=web
  TRUSTED='127.0.0.1/8 172.0.0.0/8 192.168.0.0/16'

  sed -i "s|\${HOST}|$HOST|" caddyfile.template
  sed -i "s|trusted_proxies .*|trusted_proxies $TRUSTED|" caddyfile.template
fi

chmod -R 755 ./*
mkdir -p ./assets
chown -R $USER:$USER ./assets

docker compose up -d --build --pull always
