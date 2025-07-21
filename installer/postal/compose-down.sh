#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' postal-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' postal-database)
docker-compose down -v
