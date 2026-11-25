#!/bin/bash
set -e
set -o pipefail

if ! [ -f .env ]; then
  cp .env.example .env
fi

if ! [ -d source ]; then
  git clone https://github.com/goniszewski/grimoire source
  ln -s $PWD/source/pb_migrations $PWD/migrations
fi

chmod -R 755 ./*
docker compose build
docker-compose up -d
