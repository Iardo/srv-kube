#!/bin/bash
set -e
set -o pipefail

source /.env

timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
file_sql="${timestamp}-database.sql"
file_pgdata="${timestamp}-pgdata.tar.gz"
file_opdata="${timestamp}-opdata.tar.gz"

echo "Generating: ${file_sql} ..."
PGPASSWORD=$POSTGRESQL_PASS pg_dump -h open-project-database -U $POSTGRESQL_USER -d $POSTGRESQL_NAME >> "/backups/$file_sql"
echo "Generating: ${file_pgdata} ..."
cd var/lib/postgresql/data; tar --create --gzip --file "/backups/${file_pgdata}" $(ls -A)
echo "Generating: ${file_opdata} ..."
cd /var/openproject/assets; tar --create --gzip --file "/backups/${file_opdata}" $(ls -A)
