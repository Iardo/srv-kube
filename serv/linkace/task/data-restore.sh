#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

color_green='\033[0;32m'
color_reset='\033[0m'
database_file=$1
database_name=$(basename $database_file)

# Read straight from the running container's own environment,
# not from ".env"'s dummy MYSQL_USER/MYSQL_PASS
# MariaDB only applies those at first init,
# so the DB's real credentials drift from that static file the moment
# they're rotated post-deploy (see task-sync-db-password.sh)
MYSQL_USER=$(docker exec linkace-database printenv MYSQL_USER)
MYSQL_PASS=$(docker exec linkace-database printenv MYSQL_PASSWORD)
MYSQL_NAME=$(docker exec linkace-database printenv MYSQL_DATABASE)

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
