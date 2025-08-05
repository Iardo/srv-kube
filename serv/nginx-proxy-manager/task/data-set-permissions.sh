#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

echo "Setting Permissions: /cert ..."
sudo chown -R $USER:$USER $fullpath/../cert/
echo "Setting Permissions: /data ..."
sudo chown -R $USER:$USER $fullpath/../data/
