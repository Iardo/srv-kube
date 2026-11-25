#!/bin/bash
set -e
set -o pipefail

# Globals
container_web="actual-web"
backup_archive=$(realpath $1)

# NOTE:
# Actual's data is just plain files,
# so the container is stopped first,
# writing over a file it still has open could corrupt it.
# The trap below turns it back on even if the restore fails partway.
trap 'docker start $container_web > /dev/null' EXIT

echo "File: $backup_archive"
echo "Stopping container ..."
docker stop $container_web

echo "Restoring ..."
docker run --rm --volumes-from $container_web \
  -v $backup_archive:/restore.tar.gz \
  alpine tar -xzf /restore.tar.gz -C /data

echo -e "\nRestore complete!\n"
