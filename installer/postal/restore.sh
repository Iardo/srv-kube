#!/bin/bash
set -e
set -o pipefail

# Globals
CONTAINER_WEB="postal-web"
CONTAINER_DATABASE="postal-database"
BACKUP_ARCHIVE=$1
BACKUP_BASENAME=$(basename $BACKUP_ARCHIVE .tgz)

# Logs
LOG_FOLDER="./logs"
LOG_FILE=$LOG_FOLDER/${BACKUP_BASENAME}-restore.txt
mkdir -p $LOG_FOLDER

# Restore
echo "File: $BACKUP_ARCHIVE"
echo "Extracting ..."
tar -xzf $BACKUP_ARCHIVE

echo "Importing ..."
cat $BACKUP_BASENAME/postgres.sql | \
  docker exec -i $CONTAINER_DATABASE psql -U postgres -q > $LOG_FILE
docker run --rm --volumes-from $CONTAINER_PLANKA \
  -v $(pwd)/$BACKUP_ARCHIVE:/backup ubuntu cp -rf /backup/user-avatars /app/public/
docker run --rm --volumes-from $CONTAINER_PLANKA \
  -v $(pwd)/$BACKUP_ARCHIVE:/backup ubuntu cp -rf /backup/project-background-images /app/public/
docker run --rm --volumes-from $CONTAINER_PLANKA \
  -v $(pwd)/$BACKUP_ARCHIVE:/backup ubuntu cp -rf /backup/attachments /app/private/

echo "Cleaning up temporary files ..."
rm -r $BACKUP_BASENAME

echo -e "\nRestore complete!\n"
