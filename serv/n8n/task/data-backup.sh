#!/bin/bash
set -e
set -o pipefail

# Globals
CONTAINER="n8n-database"
TIMESTAMP=$(date +"%Y.%m.%d-%H.%M.%S")

# Dump
printf "%s"   "$TIMESTAMP-database.sql | n8n | "
docker exec -t $CONTAINER pg_dumpall -c -U n8n -f /backup/$TIMESTAMP-database.sql

printf "%s\n" "Backup"
