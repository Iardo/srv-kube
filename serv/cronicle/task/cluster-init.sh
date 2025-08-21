#!/bin/bash

# https://github.com/jhuckaby/Cronicle/blob/master/docs/CommandLine.md#starting-and-stopping
# https://github.com/jhuckaby/Cronicle/blob/master/docs/Setup.md#single-server

quiet() { "$@" > /dev/null 2>&1; }
fullpath=$(dirname "$0")

docker exec -it cronicle-web ./bin/control.sh stop
docker exec -it cronicle-web ./bin/control.sh setup
docker exec -it cronicle-web ./bin/control.sh start
