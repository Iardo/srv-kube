#!/bin/bash
set -e
set -o pipefail

# Globals
container_web="linkwarden-web"
container_database="linkwarden-database"
folder_backups="./backups"
timestamp=$(date +"%Y.%m.%d-%H.%M.%S")

# Folders
mkdir -p $folder_backups
mkdir -p $timestamp-backup

# Dump
echo "File: $backup_archive"
echo "Exporting ..."
docker exec -t $container_database pg_dumpall -c -U postgres \
  > $timestamp-backup/postgres.sql

echo "Generating ..."
tar -czf $folder_backups/$timestamp-backup.tgz \
  $timestamp-backup/postgres.sql

echo "Cleaning up temporary files ..."
rm -rf $timestamp-backup

echo -e "\nBackup Complete!\n"
