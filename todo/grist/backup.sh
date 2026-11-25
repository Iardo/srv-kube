#!/bin/bash
set -e
set -o pipefail

# Docker container names
CONTAINER_WEB="grist-web"
CONTAINER_DATABASE="grist-database"
FOLDER_BACKUPS="./backups"
TIMESTAMP=$(date +"%Y.%m.%d-%H.%M.%S")

# Create Backups folder
mkdir -p $FOLDER_BACKUPS

# Create Temporary folder
mkdir -p $TIMESTAMP-backup

# Dump DB into SQL File
echo -n "Exporting database ..."
docker exec -t $CONTAINER_DATABASE pg_dumpall -c -U postgres > $TIMESTAMP-backup/postgres.sql
echo "Success!"

# Export Docker Volumes
echo -n "Exporting images-avatars ..."
docker run --rm --volumes-from $CONTAINER_WEB -v $(pwd)/$TIMESTAMP-backup:/backup ubuntu cp -r /app/public/user-avatars /backup/user-avatars
echo "Success!"
echo -n "Exporting images-background ..."
docker run --rm --volumes-from $CONTAINER_WEB -v $(pwd)/$TIMESTAMP-backup:/backup ubuntu cp -r /app/public/project-background-images /backup/project-background-images
echo "Success!"
echo -n "Exporting attachments ..."
docker run --rm --volumes-from $CONTAINER_WEB -v $(pwd)/$TIMESTAMP-backup:/backup ubuntu cp -r /app/private/attachments /backup/attachments
echo "Success!"

# Create tgz
echo -n "Generating tarball $TIMESTAMP-backup.tgz ..."
tar -czf $FOLDER_BACKUPS/$TIMESTAMP-backup.tgz \
  $TIMESTAMP-backup/postgres.sql \
  $TIMESTAMP-backup/user-avatars \
  $TIMESTAMP-backup/project-background-images \
  $TIMESTAMP-backup/attachments
echo "Success!"

# Remove source files
echo -n "Cleaning up temporary files ..."
rm -rf $TIMESTAMP-backup
echo "Success!"

echo -e "\nBackup Complete!\n"
