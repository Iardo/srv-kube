#!/bin/bash
set -e
set -o pipefail

# References
# --------------------
# https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath")

if [ -f "$rootpath/code/.installed" ]; then
  echo "llama.cpp is already installed, skipping ($rootpath/code/.installed exists)."
  exit 0
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This install script only supports Debian-based systems (needs apt-get)."
  echo "Please check llama.cpp's own build docs for your OS's package manager instead:"
  echo "https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"
  exit 1
fi

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

echo "Installing dependencies ..."
$SUDO apt-get update
$SUDO apt-get install -y build-essential cmake git libssl-dev

if [ ! -d "$rootpath/code" ]; then
  echo "Cloning llama.cpp ..."
  git clone https://github.com/ggml-org/llama.cpp "$rootpath/code"
fi

echo "Building llama.cpp ..."
cmake -B "$rootpath/code/build" -S "$rootpath/code"
cmake --build "$rootpath/code/build" --config Release -j"$(nproc)"

touch "$rootpath/code/.installed"

echo "Done. Place your .gguf model(s) under $rootpath/data/models and start the server with:"
echo "  $rootpath/code/build/bin/llama-server --model $rootpath/data/models/<model>.gguf --host 0.0.0.0 --port 8080"
