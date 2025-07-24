#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

echo "Setting Permissions: /data ..."
sudo chown -R $USER:$USER $fullpath/../data/
sudo chown -R $USER:$USER $fullpath/../logs/
