#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' epicstore-claimer)
docker-compose down -v
