#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'
folder_backups=$fullpath/../data/backup
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
database_file="${timestamp}-database.sql"

# Read straight from the running container's own environment,
# not from ".env"'s dummy MYSQL_USER/MYSQL_PASS
# MariaDB only applies those at first init,
# so the DB's real credentials drift from that static file the moment
# they're rotated post-deploy (see task-sync-db-password.sh)
MYSQL_USER=$(docker exec linkace-database printenv MYSQL_USER)
MYSQL_PASS=$(docker exec linkace-database printenv MYSQL_PASSWORD)
MYSQL_NAME=$(docker exec linkace-database printenv MYSQL_DATABASE)

mkdir -p $folder_backups

echo -e "Generating: ${color_green}$database_file${color_reset} ..."
docker exec linkace-database mariadb-dump -h linkace-database -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_NAME > $folder_backups/$database_file
