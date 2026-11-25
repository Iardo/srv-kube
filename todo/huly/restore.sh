#!/bin/bash
set -e
set -o pipefail

# Globals
CONTAINER_WEB="huly-web"
CONTAINER_DATABASE="huly-database"
BACKUP_ARCHIVE_TGZ=$1
BACKUP_ARCHIVE=$(basename $BACKUP_ARCHIVE_TGZ .tgz)

LOG_FOLDER="./logs"
LOG_FILE=$LOG_FOLDER/${BACKUP_ARCHIVE}-restore.txt

# Create Logs folder
mkdir -p $LOG_FOLDER

# Extract tgz archive
echo -n "Extracting tarball $BACKUP_ARCHIVE_TGZ ..."
tar -xzf $BACKUP_ARCHIVE_TGZ
echo "Success!"

# Import Database
echo -n "Importing database ..."
cat $BACKUP_ARCHIVE/postgres.sql | docker exec -i $CONTAINER_DATABASE psql -U postgres -q > $LOG_FILE
echo "Success!"

# Restore Docker Volumes
echo -n "Importing images-avatars ..."
docker run --rm --volumes-from $CONTAINER_WEB -v $(pwd)/$BACKUP_ARCHIVE:/backup ubuntu cp -rf /backup/user-avatars /app/public/
echo "Success!"
echo -n "Importing images-background ..."
docker run --rm --volumes-from $CONTAINER_WEB -v $(pwd)/$BACKUP_ARCHIVE:/backup ubuntu cp -rf /backup/project-background-images /app/public/
echo "Success!"
echo -n "Importing attachments ..."
docker run --rm --volumes-from $CONTAINER_WEB -v $(pwd)/$BACKUP_ARCHIVE:/backup ubuntu cp -rf /backup/attachments /app/private/
echo "Success!"

echo -n "Cleaning up temporary files and folders ..."
rm -r $BACKUP_ARCHIVE
echo "Success!"

echo -e "\nRestore complete!\n"
