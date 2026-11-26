#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
datapath=$fullpath/../data

if [ ! -d $datapath ]; then
  echo "Creating: /data ..."
  mkdir -p $datapath/srv
fi

# The image refuses to start unless these exist beforehand, it will not
# create them itself.
if [ ! -f $datapath/filebrowser.db ]; then
  echo "Creating: /data/filebrowser.db ..."
  touch $datapath/filebrowser.db
fi

if [ ! -f $datapath/settings.json ]; then
  echo "Creating: /data/settings.json ..."
  echo '{}' > $datapath/settings.json
fi
