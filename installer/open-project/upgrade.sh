#!/bin/bash
set -e
set -o pipefail

/upgrade-database.sh

echo "Please restart your installation by issuing the following command:"
echo "  docker compose up -d --build --pull always"
