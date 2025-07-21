#!/bin/bash
set -e

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' outline-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' outline-postgres)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' outline-redis)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' outline-ssl)
docker-compose down -v
