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

# A C/C++ toolchain and git have no root-free install path,
# so fail fast with an actionable message instead of running an unattended "sudo apt-get"
# (which would just hang or fail in a non-interactive deploy).
missing=""
command -v gcc >/dev/null 2>&1 && command -v g++ >/dev/null 2>&1 && command -v make >/dev/null 2>&1 || missing="$missing build-essential"
command -v git >/dev/null 2>&1 || missing="$missing git"

if [ -n "$missing" ]; then
  echo "Missing required system packages:$missing"
  echo "These need root and can't be installed automatically. Install them yourself, then re-run:"
  echo "  sudo apt-get update && sudo apt-get install -y$missing"
  exit 1
fi

if [ ! -d "$rootpath/code" ]; then
  echo "Cloning llama.cpp ..."
  git clone https://github.com/ggml-org/llama.cpp "$rootpath/code"
fi

# Cmake has an official root-free install via pip,
# so use that instead of requiring the system package.
# 
# Installed into a venv under "code".
if ! command -v cmake >/dev/null 2>&1; then
  echo "cmake not found, installing a local copy via pip (no root needed) ..."
  python3 -m venv "$rootpath/code/.cmake-venv"
  "$rootpath/code/.cmake-venv/bin/pip" install --upgrade pip cmake
  export PATH="$rootpath/code/.cmake-venv/bin:$PATH"
fi

if ! command -v cmake >/dev/null 2>&1; then
  echo "Failed to make cmake available. Install it yourself, then re-run:"
  echo "  sudo apt-get update && sudo apt-get install -y cmake"
  exit 1
fi

# NOTE:
# GPU offload needs the CUDA toolkit (nvcc), not just the driver.
#
# This is a root-only package, a "sudo apt-get" prompt
# is fine when this script is run by hand in a real terminal,
# but in an unattended/automated run it would just hang or fail silently,
# instead we detect that and print a manual command for the user instead of attempting it blindly.
cuda_flag=""
if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
  echo "NVIDIA GPU detected."
  if ! command -v nvcc >/dev/null 2>&1; then
    if [ -t 0 ] || sudo -n true 2>/dev/null; then
      echo "CUDA toolkit not found, installing (nvidia-cuda-toolkit) ..."
      if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else SUDO=""; fi
      $SUDO apt-get update
      $SUDO apt-get install -y nvidia-cuda-toolkit
    else
      echo "CUDA toolkit not found, and this is a non-interactive run so it"
      echo "can't be installed automatically. Building CPU-only for now."
      echo "To enable GPU offload, run this yourself, then re-run this install:"
      echo "  sudo apt-get update && sudo apt-get install -y nvidia-cuda-toolkit"
    fi
  fi
  if command -v nvcc >/dev/null 2>&1; then
    cuda_flag="-DGGML_CUDA=ON"
  fi
else
  echo "No NVIDIA GPU detected, building CPU-only."
fi

echo "Building llama.cpp ..."
# LLAMA_CURL=OFF drops the libcurl/openssl-dev requirement,
# which is only needed for the "-hf" auto-download flag; this setup places models by hand.
cmake -B "$rootpath/code/build" -S "$rootpath/code" -DLLAMA_CURL=OFF $cuda_flag
cmake --build "$rootpath/code/build" --config Release -j"$(nproc)"

echo "Linking llama-server/llama-cli/llama into ~/.local/bin ..."
mkdir -p "$HOME/.local/bin"
for bin in llama-server llama-cli llama; do
  ln -sf "$rootpath/code/build/bin/$bin" "$HOME/.local/bin/$bin"
done

# Models live centralized under the home directory,
# symlinked in at the path other tooling expects.
models_dir="$HOME/llms/models/llamacpp"
mkdir -p "$models_dir" "$rootpath/data"
if [ ! -e "$rootpath/data/models" ]; then
  ln -s "$models_dir" "$rootpath/data/models"
fi

# If this host declares a model list (host/<host>/data/llama-cpp/models.yml),
# symlink it in so "models.py" can read it.
for hostpath in "$rootpath"/../../host/*/data/llama-cpp/models.yml; do
  if [ -f "$hostpath" ]; then
    ln -sf "$(realpath "$hostpath")" "$rootpath/data/models.yml"
    break
  fi
done

touch "$rootpath/code/.installed"

echo "Done. Place your .gguf model(s) under $models_dir and start the server with:"
echo "  llama-server --model $models_dir/<model>.gguf --host 0.0.0.0 --port 8080"
