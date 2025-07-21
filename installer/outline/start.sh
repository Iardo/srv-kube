#!/bin/bash
set -e

if ! [ -f .env ]; then
  cp .env.sample .env
fi

# docker network inspect bridge --format='{{(index .IPAM.Config 0).Gateway}}'
docker compose up -d --build --pull always
# docker exec -it outline-web yarn db:create --env=production-ssl-disabled
# docker exec -it outline-web yarn db:migrate --env=production-ssl-disabled

# https://docs.getoutline.com/s/hosting/doc/local-development-5hEhFRXow7#h-authentication
# docker exec -it outline-web node /opt/outline/build/server/scripts/seed.js outline@gmail.com # Does not work
