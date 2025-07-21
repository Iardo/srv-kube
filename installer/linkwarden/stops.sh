#!/bin/bash
set -e

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' linkwarden-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' linkwarden-database)
docker-compose down -v
