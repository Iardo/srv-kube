#!/bin/bash
set -o pipefail

fullpath=$(dirname "$0")
python2=$(which python)
python3=$(which python3)

if [ -n "$python2" ]; then
  $python2 $fullpath/main.py "$@"
else
  $python3 $fullpath/main.py "$@"
fi
