#!/bin/bash
set -e

mkdir -p ./data
chown -R $USER:$USER ./data

docker compose up -d --build --pull always
