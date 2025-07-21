#!/bin/bash
set -e

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' aria2-pro)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' aria2-pro-ng)
docker-compose down
