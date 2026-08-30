#!/bin/bash
set -e
set -o pipefail

# Globals
container_web="planka-web"
container_database="planka-database"
fullpath=$(cd "$(dirname "$0")" && pwd)
folder_backups="$fullpath/../data/backup"
timestamp=$(date +"%Y.%m.%d-%H.%M.%S")
folder_temp="$folder_backups/$timestamp-backup"

# Folders
mkdir -p $folder_backups
mkdir -p $folder_temp

# Dump
echo "Exporting ..."
docker exec -t $container_database pg_dumpall -c -U postgres \
  > $folder_temp/postgres.sql
docker run --rm --volumes-from $container_web \
  -v $folder_temp:/backup ubuntu cp -r /app/public/user-avatars /backup/user-avatars
docker run --rm --volumes-from $container_web \
  -v $folder_temp:/backup ubuntu cp -r /app/public/project-background-images /backup/project-background-images
docker run --rm --volumes-from $container_web \
  -v $folder_temp:/backup ubuntu cp -r /app/private/attachments /backup/attachments

echo "Generating ..."
tar -czf $folder_backups/$timestamp-backup.tgz \
  -C $folder_backups $timestamp-backup

echo "Cleaning up temporary files ..."
rm -rf $folder_temp

echo -e "\nBackup Complete!\n"
