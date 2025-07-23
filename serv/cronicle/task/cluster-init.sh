#!/bin/bash

quiet() { "$@" > /dev/null 2>&1; }
fullpath=$(dirname "$0")

# https://github.com/jhuckaby/Cronicle/blob/master/docs/CommandLine.md#starting-and-stopping
# https://github.com/jhuckaby/Cronicle/blob/master/docs/Setup.md#single-server

quiet docker stop cronicle-web
$fullpath/../data/cronicle/bin/control.sh setup
quiet docker start cronicle-web
