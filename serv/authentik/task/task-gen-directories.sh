#!/bin/bash
set -e
set -o pipefail

fullpath=$(dirname "$0")

if [ ! -d $fullpath/../cert ]; then
  mkdir -p $fullpath/../cert
fi
if [ ! -d $fullpath/../data/authentik/media ]; then
  mkdir -p $fullpath/../data/authentik/media
fi
if [ ! -d $fullpath/../data/authentik/templates ]; then
  mkdir -p $fullpath/../data/authentik/templates
fi
