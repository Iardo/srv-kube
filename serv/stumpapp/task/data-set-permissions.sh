#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

sudo chown -R $USER:$USER $fullpath/../conf/
sudo chown -R $USER:$USER $fullpath/../data/
