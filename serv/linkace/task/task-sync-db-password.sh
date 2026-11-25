#!/bin/bash
set -e
set -o pipefail

# MariaDB only applies MYSQL_PASSWORD on first init of an empty volume, never
# again after that, so LINKACE_MYSQL_PASS alone drifts out of sync the moment
# it's changed post-deploy. This re-applies it every deploy, logging in as
# root with LINKACE_MYSQL_ROOT_PASS, which stays fixed forever for exactly
# this reason (see docker-compose.yml).
#
# Komodo's pre_deploy/post_deploy commands don't get the stack's
# additional_env_files exported into their shell, only the "docker compose"
# invocations themselves do.
# So the credentials are read straight from the
# already-running container's own environment (which "docker compose up -d"
# resolved correctly) instead of from $LINKACE_MYSQL_ROOT_PASS etc,
# which would otherwise be empty here.
#
# Safe to run before linkace-database exists yet (first deploy ever) or
# before it's finished starting, both are no-ops.

if ! docker ps --format '{{.Names}}' | grep -qx linkace-database; then
  exit 0
fi

root_pass=$(docker exec linkace-database printenv MYSQL_ROOT_PASSWORD)
db_user=$(docker exec linkace-database printenv MYSQL_USER)
db_pass=$(docker exec linkace-database printenv MYSQL_PASSWORD)

for i in $(seq 1 30); do
  if docker exec linkace-database mariadb -u root -p"$root_pass" -e 'SELECT 1' >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

docker exec linkace-database mariadb -u root -p"$root_pass" -e "
  ALTER USER '$db_user'@'%' IDENTIFIED BY '$db_pass';
  FLUSH PRIVILEGES;
"
