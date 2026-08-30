#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
source $fullpath/../.env
color_green='\033[0;32m'
color_reset='\033[0m'
folder_backups=$fullpath/../data/backup
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
database_file="${timestamp}-database.sql"

mkdir -p $folder_backups

echo -e "Generating: ${color_green}$database_file${color_reset} ..."
docker exec linkace-database mariadb-dump -h linkace-database -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_NAME > $folder_backups/$database_file
