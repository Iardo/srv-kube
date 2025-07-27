#!/bin/bash
set -e

if [ -f .env ]
then
  BCRYPT="$(dirname "$(realpath "$0")")"
  BCRYPT="$(realpath "$BCRYPT/../../bin/bcrypt")"
  CRED_USER=test
  CRED_PASS=test
  CRED_PASS="$($BCRYPT -c 8 $CRED_PASS)"
  CRED_PASS="$(echo $CRED_PASS | sed "s|\\$|\\$\\$|g")"
  CRED_HASH="$CRED_USER:$CRED_PASS"

  sed -i "s|TIMETAGGER_CREDENTIALS=.*|TIMETAGGER_CREDENTIALS=$CRED_HASH|" .env
fi

mkdir -p ./data
chown -R $USER:$USER ./data

chmod -R 755 ./*

docker compose up -d --build --pull always
