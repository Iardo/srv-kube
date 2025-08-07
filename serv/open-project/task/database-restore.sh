#!/bin/bash
set -e
set -o pipefail

quiet="> /dev/null 2>&1"

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'
database_path=$fullpath/../data/backup
database_file=

source $fullpath/../.env

read -p "Enter the filename: " database_file
if ! [ -f $database_path/$database_file.sql ]; then
  echo "Couldn't find the file"
  exit 0
fi

cmd_restore="\"\
DROP SCHEMA public CASCADE;\
CREATE SCHEMA public;\
\""

echo "Restoring: $database_file.sql ..."
docker exec -it open-project-database sh -c "PGPASSWORD=$POSTGRESQL_PASS psql --quiet -h localhost -U $POSTGRESQL_USER -d $POSTGRESQL_NAME -c $cmd_restore $quiet"
docker exec -it open-project-database sh -c "PGPASSWORD=$POSTGRESQL_PASS psql --quiet -h localhost -U $POSTGRESQL_USER -d $POSTGRESQL_NAME -f /backups/$database_file.sql -L /logs/$database_file-restore.log $quiet"

message=$(cat << EOF
OPEN-PROJECT: Database Restored
----
The service needs to be restarted
Please run the next command:
    ../../start.py

EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
