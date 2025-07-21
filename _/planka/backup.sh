#!/bin/bash
set -e
set -o pipefail

# Globals
CONTAINER_WEB="planka-web"
CONTAINER_DATABASE="planka-database"
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
docker run --rm --volumes-from $CONTAINER_WEB \
  -v $(pwd)/$TIMESTAMP-backup:/backup ubuntu cp -r /app/public/user-avatars /backup/user-avatars
docker run --rm --volumes-from $CONTAINER_WEB \
  -v $(pwd)/$TIMESTAMP-backup:/backup ubuntu cp -r /app/public/project-background-images /backup/project-background-images
docker run --rm --volumes-from $CONTAINER_WEB \
  -v $(pwd)/$TIMESTAMP-backup:/backup ubuntu cp -r /app/private/attachments /backup/attachments

echo "Generating ..."
tar -czf $FOLDER_BACKUPS/$TIMESTAMP-backup.tgz \
  $TIMESTAMP-backup/postgres.sql

echo "Cleaning up temporary files ..."
rm -rf $TIMESTAMP-backup

echo -e "\nBackup Complete!\n"
