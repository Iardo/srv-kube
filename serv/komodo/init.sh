#!/bin/bash
set -e
set -o pipefail

quiet() { "$@" > /dev/null 2>&1; }

fullpath="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
rootpath="$(realpath "$fullpath/../../")"
color_green='\033[0;32m'
color_reset='\033[0m'

sudo ln -sfnT "$rootpath" /etc/srv-kube

message=$(cat << EOF
Komodo: Init Done
EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
