#!/bin/bash
set -e

docker-compose stop
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-autoheal)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-backup)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-cache)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-cron)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-database)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-proxy)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-seeder)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-upgrade)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-web)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' open-project-worker)
docker-compose down
