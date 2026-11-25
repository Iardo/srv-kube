#!/bin/bash
set -e
set -o pipefail

# Globals
container_backup="open-project-backup"
fullpath=$(dirname "$0")
folder_backups="$fullpath/../data/backup"
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
source $fullpath/../.env

mkdir -p $folder_backups

echo "Generating: ${timestamp}-database.sql ..."
docker exec $container_backup sh -c "PGPASSWORD=$OPEN_PROJECT_POSTGRESQL_PASS pg_dump -h open-project-database -U $OPEN_PROJECT_POSTGRESQL_USER -d $OPEN_PROJECT_POSTGRESQL_NAME" \
  > $folder_backups/$timestamp-database.sql

echo "Generating: ${timestamp}-pgdata.tar.gz ..."
docker exec $container_backup tar -czf - -C /var/lib/postgresql/data . \
  > $folder_backups/$timestamp-pgdata.tar.gz

echo "Generating: ${timestamp}-opdata.tar.gz ..."
docker exec $container_backup tar -czf - -C /var/openproject/assets . \
  > $folder_backups/$timestamp-opdata.tar.gz

echo -e "\nBackup Complete!\n"
