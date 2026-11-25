#!/bin/bash

quiet() { "$@" > /dev/null 2>&1; }
fullpath=$(dirname "$0")

docker exec -it cronicle-web ./bin/control.sh stop
docker exec -it cronicle-web ./bin/storage-cli.js edit global/servers/0
docker exec -it cronicle-web ./bin/control.sh start
