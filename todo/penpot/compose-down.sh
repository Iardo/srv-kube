#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' penpot-backend)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' penpot-exporter)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' penpot-frontend)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' penpot-mailcatch)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' penpot-postgres)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' penpot-redis)
docker-compose down -v
