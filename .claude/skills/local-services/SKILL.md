---
name: local-services
description: Everything about how services are deployed across hosts.
---

# Local Services

- A "service" is a folder under `serv/<name>` holding that service's `docker-compose.yml`, `.env`, and any install/model scripts it needs
- `llama-cpp` and `comfyui` are GPU-bound exceptions to the general include mechanism below, see Specialized Rules: Services below for what makes them different

## General Rules

- A host under `host/<name>` picks which services it runs by listing them in its own `komodo-dpl.yml`, under `include:`, as `'${SERV:?}/<name>/${FILE:?}'`
  - `SERV` and `FILE` come from that host's `.env` (`SERV=../../serv/`, `FILE=docker-compose.yml`), so the include always resolves to `serv/<name>/docker-compose.yml`
  - Komodo merges every included compose file into that host's one stack, deployed together as `host/<name>/docker-compose.yml` (itself just `include: [...]`, see `komodo-dpl.yml`'s own leading comment)
  - Running `init.py --host <name>` after editing `komodo-dpl.yml` regenerates that host's `.env` (ports) and `.env-secrets` (per-service secrets) sections to match the new include list, they are auto-generated, not hand-edited

## Specialized Rules

Split into three groups: rules tied to a specific host rather than any one service (`### Specialized Rules: Hosts`), rules tied to a specific operating system rather than any one service (`### Specialized Rules: Operating Systems`), and rules tied to a specific service (`### Specialized Rules: Services`). One that's really about a particular machine belongs in the first group; one that would apply no matter which of these services you're installing, just because of the OS you're on, belongs in the second; one that only makes sense once you know which service you're touching belongs in the third.

### Specialized Rules: Hosts

- Each host that runs `llama-cpp` and/or `comfyui` today does so natively, none currently opt into the containerized, GPU-passthrough compose files, this is a per-host fact, not a general rule, check the table below before assuming a new host should follow either one of them
- `iardo-desktop-game-win` and `iardo-desktop-game-gnu` are the same physical machine, dual-booted between Windows and Linux, split into two separate hosts so each OS gets its own independent config (`.env`, `komodo-dpl.yml`, etc.) rather than sharing one that would only ever be half-true depending on which OS is currently booted
  - Their `komodo-srv.toml` files are the one exception, both keep the same `address = "http://iardo-desktop-game:9120"` (no `-win`/`-gnu` suffix), since only one OS can ever be booted at a time on shared hardware, there is only ever one Komodo periphery agent actually listening at that address, whichever OS is currently up

Hosts running `llama-cpp` / `comfyui` natively:

| Host                          | GPU                   | Platform | Install method |
|-------------------------------|-----------------------|----------|----------------|
| `host/iardo-macmini`          | Apple Silicon (Metal) | MacOS    | Native         |
| `host/iardo-desktop-game-win` | NVIDIA                | Windows  | Native         |
| `host/iardo-desktop-game-gnu` | NVIDIA                | Linux    | Native         |

### Specialized Rules: Operating Systems

#### Windows

- `install.bat`'s requirements differ per service, neither installs its own requirements, both fail fast with a message instead: `llama-cpp` needs Git, CMake, and Visual Studio's MSVC C/C++ build tools (the "Desktop development with C++" workload, Build Tools alone is enough, no full IDE needed); `comfyui` needs Git and Python 3 (with "Add python.exe to PATH" checked during its install)
- `llama-cpp\install.bat` additionally needs to run with the MSVC environment loaded, so `cl.exe` is on `PATH`, which a plain `cmd.exe`/PowerShell window doesn't set up on its own, unlike the Linux/MacOS `install.sh`, which needs no such step
  - Load it via the "Developer Command Prompt for VS" Start Menu shortcut, or manually with that Visual Studio install's own `vcvarsall.bat x64`, see `docs/services-gpu-bound.md` for the exact one-liners (they differ between `cmd.exe` and `powershell.exe`, see below)
  - `comfyui\install.bat` needs no such step
- `llama-cpp\install.bat` also needs the CUDA Toolkit's `nvcc` on `PATH` at build time for GPU offload, the driver alone (what `nvidia-smi` reports) isn't enough, without it the script silently builds CPU-only and `--n-gpu-layers` becomes a no-op even on a capable GPU
  - Verify with `CMakeCache.txt`'s `GGML_CUDA:BOOL` value, then install the toolkit and force a rebuild if it reads `OFF`, see `docs/services-gpu-bound.md`'s Running Server section for the exact commands
  - Symptoms of this look like a slow model rather than a broken one: GPU usage near idle during generation, RAM usage matching the model file size instead of VRAM usage, prompt processing far below what the card should give
- `cmd.exe` and `powershell.exe` are not interchangeable for these commands, a command written for one silently breaks in the other rather than erroring clearly:
  - Environment variables: `%USERPROFILE%` (`cmd.exe`) vs `$env:USERPROFILE` (PowerShell); PowerShell does not expand `%VAR%` at all, it gets passed through as a literal broken path segment instead of failing loudly
  - The `cmd /k ""path\to\file.bat" args"` doubled-leading-quote trick (works around a `cmd.exe`-specific `/k` quoting quirk) only works when the outer shell is `cmd.exe` itself; from PowerShell, use `cmd /c '"path\to\file.bat" args'` instead (single-quoted, since PowerShell's own double-quote escaping mangles the doubled-quote trick)
  - Never use `setx` to append to `PATH` from a script or one-liner, it silently truncates the value past 1024 characters and can corrupt an already-long `PATH`; use `[Environment]::SetEnvironmentVariable(...)` from PowerShell instead (even when the surrounding context is `cmd.exe`, shell out to `powershell -NoProfile -Command "..."` for this one step)
- Both `install.bat` scripts link their binaries/wrapper into `%USERPROFILE%\bin`, which is not on `PATH` by default on a fresh Windows install, so the plain `llama-server`/`comfyui` commands from Specialized Rules: Services below silently fail with "not recognized" until that folder is added, once, then a **new** terminal opened (PATH changes never apply retroactively to an already-open session)
- A linked Windows binary that exits instantly with **zero output**, not even an error, is `STATUS_DLL_NOT_FOUND` (exit code `-1073741515` / `0xC0000135`), not a bad argument or missing model file
  - `llama-server.exe` on Windows is not self-contained, it dynamically links `llama-server-impl.dll`, `llama.dll`, `ggml.dll`, `ggml-base.dll`, `ggml-cpu.dll`, `mtmd.dll`, and `llama-common.dll`, all built alongside it in `code\build\bin\Release`
  - Unlike Linux, where a symlinked binary still resolves its shared libraries through the build folder's own rpath (`$ORIGIN`-relative, which resolves against the real target file's directory, not the symlink's), Windows resolves a DLL dependency relative to whatever path the exe was actually *invoked* from, a hardlink counts as that path, so the DLLs must physically sit next to the hardlink in `%USERPROFILE%\bin`, not just in the original build folder
  - `install.bat` hardlinks (falling back to copy) every `.dll` in `code\build\bin\Release` into `%USERPROFILE%\bin` alongside the exes for exactly this reason, do not remove that step or narrow it back down to only the named executables

### Specialized Rules: Services

#### ComfyUI

- `serv/comfyui/install.sh` needs `git`, `python3`, `pip`, and `venv`; same fail-fast-with-instructions behavior as llama.cpp's script if any are missing, never an unattended `sudo apt-get`
- Builds a `.venv` under `code/.venv` and installs `code/requirements.txt` into it, then writes a `comfyui` wrapper script to `~/.local/bin` that execs `code/main.py` through that venv's Python
- Unlike llama.cpp, ComfyUI's own repo ships multiple model subfolders (`code/models/<category>/`, e.g. checkpoints, loras, vae); the install script moves each one's contents out to `$HOME/llms/models/comfyui/<category>` and symlinks it back in place, category by category, rather than symlinking a single top-level `models` folder
- The model list at `host/<host>/data/comfyui/models.yml` and `models.py` work exactly like llama.cpp's, just under `serv/comfyui/data/`
- Start it by hand once installed: `comfyui --listen 0.0.0.0`
- The containerized path (`serv/comfyui/docker-compose.yml`) runs `ghcr.io/ai-dock/comfyui:latest-cuda`, and mounts two volumes instead of one: `./data/models:/opt/ComfyUI/models` and `./data/output:/opt/ComfyUI/output`, the generated-image output folder has no equivalent in the native install, where it just lands under `code/output` inside the ComfyUI checkout itself
  - `COMFYUI_WEB_HTTP` is the published port, same auto-generated-by-`init.py` rule as `LLAMA_CPP_WEB_HTTP`

#### GPU-bound Services

- `llama-cpp` and `comfyui` each need direct GPU access (CUDA, or Apple's Metal API) for acceptable inference/generation speed
  - On a host where Docker itself cannot reach the GPU the way the machine's own OS can, most notably MacOS (Docker Desktop for Mac has no path to Metal, and no NVIDIA GPU passthrough either), these two services are installed straight onto the machine instead of run in a container
  - `serv/llama-cpp/install.sh`/`install.bat` and `serv/comfyui/install.sh`/`install.bat` do this native install (`.sh` for Linux/MacOS, `.bat` for Windows); each is meant to be run by hand on that host, not something Komodo deploys
  - `serv/llama-cpp/docker-compose.yml` and `serv/comfyui/docker-compose.yml` still exist, requesting `driver: nvidia` under `deploy.resources.reservations.devices`, but they are not this project's actual default, every host in this repo runs both services natively, including the ones with an NVIDIA GPU
    - Each compose file's own leading comment frames it as an option for "hosts where a containerized, GPU-passthrough deployment makes more sense", but in practice none of this repo's hosts have opted into that, prefer the native install unless a host explicitly asks to be the exception, see Specialized Rules: Hosts above for what each host actually does today
  - Do not add `llama-cpp` or `comfyui` to a host's `komodo-dpl.yml` `include:` list to solve a "make this host run it too" request, that swaps the native, direct-GPU install for a containerized one, which is the opposite of what these two services are set up to do here, ask first if a host genuinely needs the containerized path instead of assuming it
- Both native installs follow the same shape:
  - Clone the upstream project into `serv/<name>/code`, build or set up a venv there, and drop a `.installed` marker file in it once done, so re-running the script is a no-op
  - Symlink a centralized, per-machine model folder under `$HOME/llms/models/<name>` into `serv/<name>/data/models`, so models are never duplicated per repo clone and survive a `git pull`/reclone of this repo
  - Look for a model list at `host/<host>/data/<name>/models.yml` (the first one found, across every host folder) and symlink it to `serv/<name>/data/models.yml`, so `serv/<name>/models.py` can read it
  - `models.py` reads that `models.yml` and downloads (via `curl`) any listed model not already present in `data/models`, run it by hand after the install script, and again any time a host's `models.yml` gains new entries
  - A host's own `data/<name>/models.yml` is the only thing that actually differs per host, everything else in the install is identical, copying that one file (or the whole `data/` folder) from one host to another is how a new host adopts the same model set, but the install script still has to be run again on that new host to actually build the binaries and download the models locally, copying the file alone does not install or fetch anything
- Neither service is proxied through Caddy on a host where it's installed natively, since the running process is on the host itself, not on any Docker network, reachable directly at whatever host/port it's told to bind

#### llama.cpp

- `serv/llama-cpp/install.sh` needs a C/C++ toolchain (`build-essential`) and `git`; if missing, it prints the exact `apt-get` command and stops, it never runs a `sudo` install unattended
  - It also installs `cmake` itself, into a local venv under `code/.cmake-venv`, if the system doesn't already have it, no root needed for that part
  - If an NVIDIA GPU is detected (`nvidia-smi` succeeds) but `nvcc` (the CUDA toolkit) is missing, it tries `sudo apt-get install -y nvidia-cuda-toolkit` only when running interactively or already passwordless-sudo, otherwise it builds CPU-only and prints the manual command to enable GPU offload later
  - Builds with `cmake -DGGML_CUDA=ON` when CUDA is available, `-DLLAMA_CURL=OFF` always (this setup places `.gguf` files by hand, so the `-hf` auto-download flag, and its `libcurl`/`openssl-dev` dependency, is never needed)
  - Links `llama-server`, `llama-cli`, and `llama` into `~/.local/bin` (`%USERPROFILE%\bin` on Windows, see Specialized Rules: Operating Systems above for why the Windows install also needs to link every `.dll` there, not just the exes)
  - Models live at `$HOME/llms/models/llamacpp`, symlinked to `serv/llama-cpp/data/models`
  - Start the server by hand once installed, text-only: `llama-server --model $HOME/llms/models/llamacpp/<model>.gguf --host 0.0.0.0 --port 8080`
  - With GPU offload and vision/file input, needs the model's own `--mmproj` file (some models ship one, e.g. `models.yml`'s `*-mmproj-f16.gguf` entries): `llama-server --model $HOME/llms/models/llamacpp/<model>.gguf --mmproj $HOME/llms/models/llamacpp/<model-mmproj>.gguf --n-gpu-layers 999 --host 0.0.0.0 --port 8080`
- The containerized path (`serv/llama-cpp/docker-compose.yml`) runs `ghcr.io/ggml-org/llama.cpp:server`, mounts `./data/models:/models`, and requires `LLAMA_CPP_MODEL` (the `.gguf` filename under `data/models`) to be set, since the compose command references `/models/${LLAMA_CPP_MODEL:?}`, an unset value fails the deploy outright rather than silently picking a default
  - Set it as a host `.env` override, under that host's own "Override" section, not inside `serv/llama-cpp/.env`, which only ships the dummy `changeme.gguf` default
  - `LLAMA_CPP_WEB_HTTP` is the published port, auto-generated by `init.py` into the host's `.env`, do not hand-edit it
