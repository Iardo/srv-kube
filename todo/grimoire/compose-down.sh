#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grimoire-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grimoire-pocketbase)
docker-compose down -v
