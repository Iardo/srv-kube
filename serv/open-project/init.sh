#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'

quiet sh -c $fullpath/task/data-gen-directories.sh
quiet sh -c $fullpath/task/data-set-permissions.sh

message=$(cat << EOF
OPEN-PROJECT: Init Done
----
The setup requires some manual steps
Once the container is running:
    cd /serv/open-project
    sh -c ./task/data-delete-demo-projects.sh
EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
