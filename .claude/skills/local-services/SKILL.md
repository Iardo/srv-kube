---
name: local-services
description: Everything about how services are deployed across hosts.
---

# Local Services

- A "service" is a folder under `serv/<name>` holding that service's `docker-compose.yml`, `.env`, and any install/model scripts it needs
- `llama-cpp` and `comfyui` are GPU-bound exceptions to the general include mechanism below, see Specialized Rules: GPU-bound Services for what makes them different

## General Rules

- A host under `host/<name>` picks which services it runs by listing them in its own `komodo-dpl.yml`, under `include:`, as `'${SERV:?}/<name>/${FILE:?}'`
  - `SERV` and `FILE` come from that host's `.env` (`SERV=../../serv/`, `FILE=docker-compose.yml`), so the include always resolves to `serv/<name>/docker-compose.yml`
  - Komodo merges every included compose file into that host's one stack, deployed together as `host/<name>/docker-compose.yml` (itself just `include: [...]`, see `komodo-dpl.yml`'s own leading comment)
  - Running `init.py --host <name>` after editing `komodo-dpl.yml` regenerates that host's `.env` (ports) and `.env-secrets` (per-service secrets) sections to match the new include list, they are auto-generated, not hand-edited

## Specialized Rules

### Specialized Rules: GPU-bound Services

- `llama-cpp` and `comfyui` each need direct GPU access (CUDA, or Apple's Metal API) for acceptable inference/generation speed
  - On a host where Docker itself cannot reach the GPU the way the machine's own OS can, most notably macOS (Docker Desktop for Mac has no path to Metal, and no NVIDIA GPU passthrough either), these two services are installed straight onto the machine instead of run in a container
  - `serv/llama-cpp/install.sh` and `serv/comfyui/install.sh` do this native install; each is a normal bash script meant to be run by hand on that host, not something Komodo deploys
  - `serv/llama-cpp/docker-compose.yml` and `serv/comfyui/docker-compose.yml` still exist, requesting `driver: nvidia` under `deploy.resources.reservations.devices`, but they are not this project's actual default, every host in this repo runs both services natively, including the ones with an NVIDIA GPU
    - Each compose file's own leading comment frames it as an option for "hosts where a containerized, GPU-passthrough deployment makes more sense", but in practice none of this repo's hosts have opted into that, prefer the native install unless a host explicitly asks to be the exception, see Specialized Rules: Hosts below for what each host actually does today
  - Do not add `llama-cpp` or `comfyui` to a host's `komodo-dpl.yml` `include:` list to solve a "make this host run it too" request, that swaps the native, direct-GPU install for a containerized one, which is the opposite of what these two services are set up to do here, ask first if a host genuinely needs the containerized path instead of assuming it
  - `serv/llama-cpp/install.sh` targets a Debian-based Linux host (`apt-get`, `build-essential`, optional CUDA toolkit); it has no Windows path, a Windows host (like `iardo-desktop-game-win`) needing llama.cpp natively needs its own install approach (a prebuilt Windows release, or building with MSVC/CUDA directly), not a straight run of this script
- Both native installs follow the same shape:
  - Clone the upstream project into `serv/<name>/code`, build or set up a venv there, and drop a `.installed` marker file in it once done, so re-running the script is a no-op
  - Symlink a centralized, per-machine model folder under `$HOME/llms/models/<name>` into `serv/<name>/data/models`, so models are never duplicated per repo clone and survive a `git pull`/reclone of this repo
  - Look for a model list at `host/<host>/data/<name>/models.yml` (the first one found, across every host folder) and symlink it to `serv/<name>/data/models.yml`, so `serv/<name>/models.py` can read it
  - `models.py` reads that `models.yml` and downloads (via `curl`) any listed model not already present in `data/models`, run it by hand after the install script, and again any time a host's `models.yml` gains new entries
  - A host's own `data/<name>/models.yml` is the only thing that actually differs per host, everything else in the install is identical, copying that one file (or the whole `data/` folder) from one host to another is how a new host adopts the same model set, but the install script still has to be run again on that new host to actually build the binaries and download the models locally, copying the file alone does not install or fetch anything
- Neither service is proxied through Caddy on a host where it's installed natively, since the running process is on the host itself, not on any Docker network, reachable directly at whatever host/port it's told to bind

### Specialized Rules: Hosts

- Each host that runs `llama-cpp` and/or `comfyui` today does so natively, none currently opt into the containerized, GPU-passthrough compose files, this is a per-host fact, not a general rule, check this table before assuming a new host should follow either one of them
- `iardo-desktop-game-win` and `iardo-desktop-game-gnu` are the same physical machine, dual-booted between Windows and Linux, split into two separate hosts so each OS gets its own independent config (`.env`, `komodo-dpl.yml`, etc.) rather than sharing one that would only ever be half-true depending on which OS is currently booted
  - Their `komodo-srv.toml` files are the one exception, both keep the same `address = "http://iardo-desktop-game:9120"` (no `-win`/`-gnu` suffix), since only one OS can ever be booted at a time on shared hardware, there is only ever one Komodo periphery agent actually listening at that address, whichever OS is currently up

#### Hosts running `llama-cpp` / `comfyui` natively

| Host                          | GPU                   | Platform | Install method |
|-------------------------------|-----------------------|----------|----------------|
| `host/iardo-macmini`          | Apple Silicon (Metal) | macOS    | Native         |
| `host/iardo-desktop-game-win` | NVIDIA                | Windows  | Native         |
| `host/iardo-desktop-game-gnu` | NVIDIA                | Linux    | Native         |

### Specialized Rules: llama.cpp

- `serv/llama-cpp/install.sh` needs a C/C++ toolchain (`build-essential`) and `git`; if missing, it prints the exact `apt-get` command and stops, it never runs a `sudo` install unattended
  - It also installs `cmake` itself, into a local venv under `code/.cmake-venv`, if the system doesn't already have it, no root needed for that part
  - If an NVIDIA GPU is detected (`nvidia-smi` succeeds) but `nvcc` (the CUDA toolkit) is missing, it tries `sudo apt-get install -y nvidia-cuda-toolkit` only when running interactively or already passwordless-sudo, otherwise it builds CPU-only and prints the manual command to enable GPU offload later
  - Builds with `cmake -DGGML_CUDA=ON` when CUDA is available, `-DLLAMA_CURL=OFF` always (this setup places `.gguf` files by hand, so the `-hf` auto-download flag, and its `libcurl`/`openssl-dev` dependency, is never needed)
  - Links `llama-server`, `llama-cli`, and `llama` into `~/.local/bin`
  - Models live at `$HOME/llms/models/llamacpp`, symlinked to `serv/llama-cpp/data/models`
  - Start the server by hand once installed: `llama-server --model $HOME/llms/models/llamacpp/<model>.gguf --host 0.0.0.0 --port 8080`
- The containerized path (`serv/llama-cpp/docker-compose.yml`) runs `ghcr.io/ggml-org/llama.cpp:server`, mounts `./data/models:/models`, and requires `LLAMA_CPP_MODEL` (the `.gguf` filename under `data/models`) to be set, since the compose command references `/models/${LLAMA_CPP_MODEL:?}`, an unset value fails the deploy outright rather than silently picking a default
  - Set it as a host `.env` override, under that host's own "Override" section, not inside `serv/llama-cpp/.env`, which only ships the dummy `changeme.gguf` default
  - `LLAMA_CPP_WEB_HTTP` is the published port, auto-generated by `init.py` into the host's `.env`, do not hand-edit it

### Specialized Rules: ComfyUI

- `serv/comfyui/install.sh` needs `git`, `python3`, `pip`, and `venv`; same fail-fast-with-instructions behavior as llama.cpp's script if any are missing, never an unattended `sudo apt-get`
- Builds a `.venv` under `code/.venv` and installs `code/requirements.txt` into it, then writes a `comfyui` wrapper script to `~/.local/bin` that execs `code/main.py` through that venv's Python
- Unlike llama.cpp, ComfyUI's own repo ships multiple model subfolders (`code/models/<category>/`, e.g. checkpoints, loras, vae); the install script moves each one's contents out to `$HOME/llms/models/comfyui/<category>` and symlinks it back in place, category by category, rather than symlinking a single top-level `models` folder
- The model list at `host/<host>/data/comfyui/models.yml` and `models.py` work exactly like llama.cpp's, just under `serv/comfyui/data/`
- Start it by hand once installed: `comfyui --listen 0.0.0.0`
- The containerized path (`serv/comfyui/docker-compose.yml`) runs `ghcr.io/ai-dock/comfyui:latest-cuda`, and mounts two volumes instead of one: `./data/models:/opt/ComfyUI/models` and `./data/output:/opt/ComfyUI/output`, the generated-image output folder has no equivalent in the native install, where it just lands under `code/output` inside the ComfyUI checkout itself
  - `COMFYUI_WEB_HTTP` is the published port, same auto-generated-by-`init.py` rule as `LLAMA_CPP_WEB_HTTP`
