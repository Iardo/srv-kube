#!/bin/bash
set -e
set -o pipefail

source /.env

quiet() { "$@" > /dev/null 2>&1; }

timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
file_sql="${timestamp}-database.sql"

echo "Generating: ${file_sql} ..."
docker exec -it linkace-database sh -c "\
  mariadb-dump\
    -h linkace-database \
    -U $MYSQL_USER \
    -p$MYSQL_PASS \
    -d $MYSQL_NAME \
  >> \"/backups/$file_sql\"
  "
