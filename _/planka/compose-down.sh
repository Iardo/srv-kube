#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' planka-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' planka-database)
docker-compose down -v
