#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' infisical-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' infisical-database)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' infisical-migration)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' infisical-redis)
docker-compose down -v
