#!/bin/bash
set -e
set -o pipefail

# Globals
container_database="n8n-database"
fullpath=$(dirname "$0")
folder_backups="$fullpath/../data/backup"
timestamp=$(date +"%Y.%m.%d-%H.%M.%S")

mkdir -p $folder_backups

# Dump
printf "%s"   "$timestamp-database.sql | n8n | "
docker exec $container_database pg_dumpall -c -U n8n > $folder_backups/$timestamp-database.sql

printf "%s\n" "Backup"
