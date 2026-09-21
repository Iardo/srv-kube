#!/bin/bash
set -e
set -o pipefail

root_dir=$(dirname "$0")
root_dir=$(realpath "$root_dir/..")

for adapter in claude roo; do
  ln -sfn .llms "$root_dir/.$adapter"
done

# Claude Code only auto-loads CLAUDE.md from the project root
ln -sfn .llms/AGENTS.md "$root_dir/CLAUDE.md"
