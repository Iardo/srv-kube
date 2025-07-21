#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' paperless-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' paperless-database)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' paperless-broker)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' paperless-gotenberg)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' paperless-tika)
docker-compose down -v
