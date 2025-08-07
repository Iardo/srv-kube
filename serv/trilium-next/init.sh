#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")
color_green='\033[0;32m'
color_reset='\033[0m'

sh -c $fullpath/task/data-gen-directories.sh
sh -c $fullpath/task/data-set-permissions.sh
echo ''

message=$(cat << EOF
TRILLIUM-NEXT: Init Done
----
The setup requires some manual steps
Once the container is running:
- cd /serv/trillium-next
- sh -c ./task/data-set-permissions.sh

EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"