#!/bin/bash
set -e
set -o pipefail

# Globals
CONTAINER_WEB="linkwarden-web"
CONTAINER_DATABASE="linkwarden-database"
FOLDER_BACKUPS="./backups"
TIMESTAMP=$(date +"%Y.%m.%d-%H.%M.%S")

# Folders
mkdir -p $FOLDER_BACKUPS
mkdir -p $TIMESTAMP-backup

# Dump
echo "File: $BACKUP_ARCHIVE"
echo "Exporting ..."
docker exec -t $CONTAINER_DATABASE pg_dumpall -c -U postgres \
  > $TIMESTAMP-backup/postgres.sql

echo "Generating ..."
tar -czf $FOLDER_BACKUPS/$TIMESTAMP-backup.tgz \
  $TIMESTAMP-backup/postgres.sql

echo "Cleaning up temporary files ..."
rm -rf $TIMESTAMP-backup

echo -e "\nBackup Complete!\n"
