#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' passbolt-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' passbolt-database)
docker-compose down -v
