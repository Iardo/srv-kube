#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'
database_file=$1
database_name=$(basename $database_file)
log_file="$fullpath/../data/backup/${database_name}-restore.txt"
source $fullpath/../.env

if ! [ -f $database_file ]; then
  echo "Couldn't find the file"
  exit 0
fi

cmd_restore="\"\
DROP SCHEMA public CASCADE;\
CREATE SCHEMA public;\
\""

echo "Restoring: $database_name ..."
docker exec open-project-database sh -c "PGPASSWORD=$OPEN_PROJECT_POSTGRESQL_PASS psql --quiet -h localhost -U $OPEN_PROJECT_POSTGRESQL_USER -d $OPEN_PROJECT_POSTGRESQL_NAME -c $cmd_restore" > /dev/null 2>&1
docker exec -i open-project-database sh -c "PGPASSWORD=$OPEN_PROJECT_POSTGRESQL_PASS psql --quiet -h localhost -U $OPEN_PROJECT_POSTGRESQL_USER -d $OPEN_PROJECT_POSTGRESQL_NAME" < $database_file > $log_file 2>&1

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
