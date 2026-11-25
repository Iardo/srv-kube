#!/bin/bash
set -e
set -o pipefail

PG_DATA_DIR="/var/lib/postgresql/data"
PG_WORK_DIR="/var/lib/postgresql/work"
PG_VERSION_NOW="$(cat /var/lib/postgresql/data/PG_VERSION)"
PG_VERSION_NEW="13"

if [ ! "$PG_VERSION_NOW" -lt "$PG_VERSION_NEW" ]; then
	echo "Current PG version is higher or equal to the PG version to be installed ($PG_VERSION_NOW > $PG_VERSION_NEW). Ignoring."
	exit 0
fi

export PG_BIN_OLD="/usr/lib/postgresql/$PG_VERSION_NOW/bin"
export PG_BIN_NEW="/usr/lib/postgresql/$PG_VERSION_NEW/bin"
export PG_DATA_OLD="$PG_DATA_DIR"
export PG_DATA_NEW="$PG_WORK_DIR/datanew"

rm -rf "$PG_WORK_DIR" && mkdir -p "$PG_WORK_DIR" "$PG_DATA_NEW"
chown -R postgres.postgres "$PG_DATA_DIR" "$PG_WORK_DIR"
cd "$PG_WORK_DIR"

su -m postgres -c "$PG_BIN_NEW/initdb --pgdata=$PG_DATA_NEW --encoding=unicode --auth=trust"
su -m postgres -c "$PG_BIN_NEW/pg_upgrade -c"
su -m postgres -c "$PG_BIN_NEW/pg_upgrade"
su -m postgres -c "rm -rf $PG_DATA_OLD/* && mv $PGDATANEW/* $PG_DATA_OLD/"
su -m postgres -c "echo \"listen_addresses = '*'\" >> $PG_DATA_OLD/postgresql.conf"
su -m postgres -c "echo \"host all all all md5\" >> $PG_DATA_OLD/pg_hba.conf"

echo "Please restart your installation by issuing the following command:"
echo "- docker compose up -d --build --pull always"
