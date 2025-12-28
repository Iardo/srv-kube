#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'

quiet sh -c $fullpath/task/task-gen-directories.sh
quiet sh -c $fullpath/task/task-set-permissions.sh

message=$(cat << EOF
CRONJOB-ORG: Init Done
EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
