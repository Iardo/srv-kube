#!/bin/bash

ROOT="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Export for tr error in mac
export LC_ALL=C
export LC_CTYPE=C

if ! [ -d source ]; then
  git clone https://github.com/makeplane/plane.git
  mv plane source
fi

if ! [ -f .env ]; then
  ln -s $ROOT/.env.example $ROOT/.env
  ln -s $ROOT/.env.example $ROOT/source/.env
fi
if ! [ -f ./source/admin/.env ]; then
  ln -s $ROOT/.env.example.admin $ROOT/source/admin/.env
fi
if ! [ -f ./source/apiserver/.env ]; then
  ln -s $ROOT/.env.example.apiserver $ROOT/source/apiserver/.env
fi
if ! [ -f ./source/space/.env ]; then
  ln -s $ROOT/.env.example.space $ROOT/source/space/.env
fi
if ! [ -f ./source/web/.env ]; then
  ln -s $ROOT/.env.example.web $ROOT/source/web/.env
fi

# Generate the SECRET_KEY that will be used by django
echo "SECRET_KEY=\"$(tr -dc 'a-z0-9' < /dev/urandom | head -c50)\""  >> ./source/apiserver/.env

docker-compose up -d
