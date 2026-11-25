#!/bin/bash
set -e
set -o pipefail

# Read straight from the running container's own environment,
# which came from this host's ".env-secrets"/".env-secrets.local"
# (see readme.md), not from "serv/passbolt/.env".
PASSBOLT_ADMIN_EMAIL=$(docker exec passbolt-web printenv PASSBOLT_ADMIN_EMAIL)
PASSBOLT_ADMIN_FIRSTNAME=$(docker exec passbolt-web printenv PASSBOLT_ADMIN_FIRSTNAME)
PASSBOLT_ADMIN_LASTNAME=$(docker exec passbolt-web printenv PASSBOLT_ADMIN_LASTNAME)

if [ -z "$PASSBOLT_ADMIN_EMAIL" ] || [ -z "$PASSBOLT_ADMIN_FIRSTNAME" ] || [ -z "$PASSBOLT_ADMIN_LASTNAME" ]; then
  echo "PASSBOLT_ADMIN_EMAIL/FIRSTNAME/LASTNAME are empty, fill them in this host's .env-secrets.local and redeploy first (see readme.md)."
  exit 1
fi

# The "-non-root" image already runs as "www-data" by default,
# "su" would just prompt for a password it doesn't have
# (see passbolt_docker's own README, "Or alternatively for non-root image").
docker exec -it passbolt-web /usr/share/php/passbolt/bin/cake passbolt register_user -u "$PASSBOLT_ADMIN_EMAIL" -f "$PASSBOLT_ADMIN_FIRSTNAME" -l "$PASSBOLT_ADMIN_LASTNAME" -r admin
