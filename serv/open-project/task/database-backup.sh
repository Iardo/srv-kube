#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

docker exec -it open-project-backup sh -c "/backup.sh"
