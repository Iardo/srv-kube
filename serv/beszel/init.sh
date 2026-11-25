#!/bin/bash
set -e
set -o pipefail

color_green='\033[0;32m'
color_reset='\033[0m'

message=$(cat << EOF
BESZEL: Init Done
----
The setup requires some manual steps, "beszel-agent" needs a TOKEN/KEY that
only exist once the Hub is already running: see serv/beszel/readme.md
EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
