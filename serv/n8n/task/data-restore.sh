#!/bin/bash
set -e
set -o pipefail

# Globals
CONTAINER="n8n-database"
SQLIMPORT=$1

# Commands
printf "%s"   "$SQLIMPORT | n8n | "
# docker exec -i $CONTAINER_DATABASE psql -U n8n -f /backup/$SQLIMPORT -q > /logs/${SQLIMPORT}.txt # TODO: needs testing

printf "%s\n" "Restored"
