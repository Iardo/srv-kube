#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
source $fullpath/../.env
color_green='\033[0;32m'
color_reset='\033[0m'
database_file=$1
database_name=$(basename $database_file)
database_drop="\"DROP DATABASE $MYSQL_NAME; CREATE DATABASE $MYSQL_NAME;\""

if ! [ -f $database_file ]; then
  echo "Couldn't find the file"
  exit 0
fi

echo ""
echo -e "Restoring: ${color_green}$database_name${color_reset} ..."
quiet docker exec linkace-web php artisan setup:complete
docker exec linkace-database sh -c "mariadb -h localhost -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_NAME -e $database_drop"
docker exec -i linkace-database mariadb -h localhost -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_NAME < $database_file
