#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-account)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-collaborator)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-database)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-elasticsearch)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-minio)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-rekoni)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' huly-transactor)
docker-compose down -v
