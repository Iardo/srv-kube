#!/bin/bash

quiet() { "$@" > /dev/null 2>&1; }
fullpath=$(dirname "$0")

docker exec -it cronicle-web /bin/sh -c "\
  apk add sshpass;\
"
