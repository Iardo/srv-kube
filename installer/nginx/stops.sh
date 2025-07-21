#!/bin/bash
set -e

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' nginx)
docker-compose down -v
