#!/bin/bash
set -e
set -o pipefail

# Globals
container_web="planka-web"
container_database="planka-database"
fullpath=$(cd "$(dirname "$0")" && pwd)
backup_archive=$1
backup_basename=$(basename $backup_archive .tgz)
folder_backups="$fullpath/../data/backup"
log_file=$folder_backups/${backup_basename}-restore.txt

mkdir -p $folder_backups

# Restore
echo "File: $backup_archive"
echo "Extracting ..."
tar -xzf $backup_archive -C $folder_backups

echo "Importing ..."
cat $folder_backups/$backup_basename/postgres.sql | \
  docker exec -i $container_database psql -U postgres -q > $log_file
docker run --rm --volumes-from $container_web \
  -v $folder_backups/$backup_basename:/backup ubuntu cp -rf /backup/user-avatars /app/public/
docker run --rm --volumes-from $container_web \
  -v $folder_backups/$backup_basename:/backup ubuntu cp -rf /backup/project-background-images /app/public/
docker run --rm --volumes-from $container_web \
  -v $folder_backups/$backup_basename:/backup ubuntu cp -rf /backup/attachments /app/private/

echo "Cleaning up temporary files ..."
rm -rf $folder_backups/$backup_basename

echo -e "\nRestore complete!\n"
