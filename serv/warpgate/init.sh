#!/bin/bash
set -e
set -o pipefail

color_green='\033[0;32m'
color_reset='\033[0m'

message=$(cat << EOF
WARPGATE: Init Done
----
The setup requires some manual steps
Once this service's compose file exists but BEFORE the first "docker compose up":
    > cd serv/warpgate
    > docker run --rm -it -v ./data:/data ghcr.io/warp-tech/warpgate:0.30.6 setup
      (interactive, generates data/warpgate.yaml and the admin password)
EOF
)

echo -e "\
${color_green}\
${message}\
${color_reset}
"
