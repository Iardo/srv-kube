#!/bin/bash
set -e
set -o pipefail

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grist-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grist-database)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grist-redis)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grist-minio)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' grist-minio-setup)
docker-compose down -v
