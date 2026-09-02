#!/bin/bash
set -e
set -o pipefail

# References
# --------------------
# https://docs.comfy.org/installation/manual_install

fullpath=$(dirname "$0")
rootpath=$(realpath "$fullpath")

if [ -f "$rootpath/code/.installed" ]; then
  echo "ComfyUI is already installed, skipping ($rootpath/code/.installed exists)."
  exit 0
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This install script only supports Debian-based systems (needs apt-get)."
  echo "Please check ComfyUI's own install docs for your OS's package manager instead:"
  echo "https://docs.comfy.org/installation/manual_install"
  exit 1
fi

if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi

echo "Installing dependencies ..."
$SUDO apt-get update
$SUDO apt-get install -y git python3 python3-pip python3-venv

if [ ! -d "$rootpath/code" ]; then
  echo "Cloning ComfyUI ..."
  git clone https://github.com/comfyanonymous/ComfyUI.git "$rootpath/code"
fi

echo "Creating virtual environment ..."
python3 -m venv "$rootpath/code/.venv"
source "$rootpath/code/.venv/bin/activate"
pip install --upgrade pip wheel
pip install -r "$rootpath/code/requirements.txt"
deactivate

touch "$rootpath/code/.installed"

echo "Done. Start it with:"
echo "  cd $rootpath/code && source .venv/bin/activate && python3 main.py --listen 0.0.0.0"
