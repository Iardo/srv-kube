#!/bin/bash
set -e
set -o pipefail

# Globals
container_web="actual-web"
fullpath=$(cd "$(dirname "$0")" && pwd)
folder_backups="$fullpath/../data/backup"
timestamp=$(date +"%Y.%m.%d-%H.%M.%S")

# NOTE:
# Actual has no database container.
# Its data is just files under /data,
# "server-files" holds the app's own account.sqlite,
# "user-files" holds one file per budget.
# Backing up means zipping those folders as they are.
mkdir -p $folder_backups

echo "Exporting ..."
docker exec $container_web tar -czf - -C /data server-files user-files \
  > $folder_backups/$timestamp-data.tar.gz

echo -e "\nBackup Complete!\n"
