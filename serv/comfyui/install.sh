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

# None of these have a root-free install path,
# so fail fast with an actionable message instead of running an unattended "sudo apt-get"
# which would just hang or fail in a non-interactive deploy.
missing=""
command -v git >/dev/null 2>&1 || missing="$missing git"
command -v python3 >/dev/null 2>&1 || missing="$missing python3"
python3 -m pip --version >/dev/null 2>&1 || missing="$missing python3-pip"
python3 -m venv --help >/dev/null 2>&1 || missing="$missing python3-venv"

if [ -n "$missing" ]; then
  echo "Missing required system packages:$missing"
  echo "These need root and can't be installed automatically. Install them yourself, then re-run:"
  echo "  sudo apt-get update && sudo apt-get install -y$missing"
  exit 1
fi

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

echo "Adding 'comfyui' command to ~/.local/bin ..."
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/comfyui" <<WRAPPER
#!/bin/bash
exec "$rootpath/code/.venv/bin/python3" "$rootpath/code/main.py" "\$@"
WRAPPER
chmod +x "$HOME/.local/bin/comfyui"

# Models live centralized under the home directory (shared across any repo
# clone/host on this machine), one category subfolder at a time, matching
# ComfyUI's own "code/models/<category>" layout.
models_root="$HOME/llms/models/comfyui"
mkdir -p "$models_root"
for category_dir in "$rootpath"/code/models/*/; do
  category_dir="${category_dir%/}"
  category=$(basename "$category_dir")
  if [ -L "$category_dir" ]; then
    continue
  fi
  mkdir -p "$models_root/$category"
  find "$category_dir" -mindepth 1 -maxdepth 1 -exec mv {} "$models_root/$category/" \;
  rmdir "$category_dir"
  ln -s "$models_root/$category" "$category_dir"
done

# If this host declares a model list (host/<host>/data/comfyui/models.yml),
# symlink it in so "models.py" can read it.
mkdir -p "$rootpath/data"
if [ ! -e "$rootpath/data/models" ]; then
  ln -s "$models_root" "$rootpath/data/models"
fi
for hostpath in "$rootpath"/../../host/*/data/comfyui/models.yml; do
  if [ -f "$hostpath" ]; then
    ln -sf "$(realpath "$hostpath")" "$rootpath/data/models.yml"
    break
  fi
done

touch "$rootpath/code/.installed"

echo "Done. Start it with:"
echo "  comfyui --listen 0.0.0.0"
