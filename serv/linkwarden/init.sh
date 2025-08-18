#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'

quiet sh -c $fullpath/task/data-gen-directories.sh

message=$(cat << EOF
LINKWARDEN: Init Done
EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
