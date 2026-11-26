#!/bin/bash
set -e
set -o pipefail

# maddy refuses to start without /data/tls/fullchain.pem + privkey.pem
# (it has no cert of its own, unlike most web services here fronted by Caddy).
# Generates a self-signed pair if one isn't already there, never overwrites.
# Replace with a real cert for real deliverability, see readme.md.

tls_dir="$(dirname "$0")/../data/tls"

if [ -f "$tls_dir/fullchain.pem" ] && [ -f "$tls_dir/privkey.pem" ]; then
  exit 0
fi

mkdir -p "$tls_dir"

openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
  -keyout "$tls_dir/privkey.pem" \
  -out "$tls_dir/fullchain.pem" \
  -subj "/CN=${MADDY_HOSTNAME:-maddy.local}"
