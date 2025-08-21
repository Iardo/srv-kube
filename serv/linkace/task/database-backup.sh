#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
source $fullpath/../.env
color_green='\033[0;32m'
color_reset='\033[0m'
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
database_file="${timestamp}-database.sql"

echo -e "Generating: ${color_green}$database_file.sql${color_reset} ..."
docker exec linkace-database sh -c "mariadb-dump -h linkace-database -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_NAME >> \"/backups/$database_file\""
