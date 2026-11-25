#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

source $fullpath/../.env

docker exec -it passbolt-web su -m -c "/usr/share/php/passbolt/bin/cake passbolt register_user -u $PASSBOLT_ADMIN_EMAIL -f $PASSBOLT_ADMIN_FIRSTNAME -l $PASSBOLT_ADMIN_LASTNAME -r admin" -s /bin/sh www-data
