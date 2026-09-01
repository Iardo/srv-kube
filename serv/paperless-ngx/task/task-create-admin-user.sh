#!/bin/bash
set -e
set -o pipefail

docker exec -it paperless-ngx-web python3 manage.py createsuperuser
