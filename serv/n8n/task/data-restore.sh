#!/bin/bash
set -e
set -o pipefail

# Globals
container_database="n8n-database"
sql_import=$1

# Commands
printf "%s"   "$sql_import | n8n | "
docker exec -i $container_database psql -U n8n -q < $sql_import

printf "%s\n" "Restored"
