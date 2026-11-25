#!/bin/bash
set -e
set -o pipefail

# Globals
container_web="azimutt-web"
container_database="azimutt-database"
backup_archive=$1
backup_basename=$(basename $backup_archive .tgz)

# Logs
log_folder="./logs"
log_file=$log_folder/${backup_basename}-restore.txt
mkdir -p $log_folder

# Restore
echo "File: $backup_archive"
echo "Extracting ..."
tar -xzf $backup_archive

echo "Importing ..."
cat $backup_basename/postgres.sql | \
  docker exec -i $container_database psql -U postgres -q > $log_file

echo "Cleaning up temporary files ..."
rm -r $backup_basename

echo -e "\nRestore complete!\n"
