#!/bin/sh
# Auto generated running init.py,
# Do not edit by hand, changes get overwritten on the next run.
#
# One-time (per machine) setup so every "*.<host-name>" domain
# below resolves to 127.0.0.1. Needs sudo.
set -e

PORT=8000
DOMAINS="iardo-vps-iardodev"

sudo mkdir -p /etc/systemd/resolved.conf.d
printf '[Resolve]\nDNS=127.0.0.1:%s\nDomains=%s\n' "$PORT" "$(echo "$DOMAINS" | sed 's/[^ ]*/~&/g')" \
  | sudo tee /etc/systemd/resolved.conf.d/dnsmasq-wildcards.conf
sudo systemctl restart systemd-resolved
