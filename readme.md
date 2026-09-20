# Dockerfiles

Collection of docker files for a lot of different services.

---

## How it Works

Two ways to deploy:
- Running `./start.py` (local, one host at a time)
- Using Komodo (web UI, deploys to any machine, auto-redeploys on git push).

Komodo is optional,
Komodo itself is just another service in this repo.

First time cloning the repo: run `./start.py`, pick a host, install Komodo on it.
From then on, use Komodo for every other host.
You can always fall back to `./start.py` for any host, Komodo or not.

---

## Host Config

Copy `/host/@host-sample` to make a new host, it has:
```
docker-compose.yml  : Which services to install (the "include" list)
.env                : Non-secret overrides (ports, timezone, etc), the ports section is auto-generated
.env-secrets        : One dummy value per secret var, tracked in git, just a reference
.env-secrets.local  : Gitignored, real secret values go here, never wiped by a re-deploy
```

The file `.env-secrets.local` is what you edit by hand (or over SSH on a VPS) to put real values in.\
Komodo copies `.env-secrets` into it automatically the first time, so it's ready to fill in.\
It always wins over `.env-secrets` when both set the same variable.

---

## Scripts

```
./init.py  : One-time setup, generates ports, runs each service's init.sh
./start.py : Docker compose up for a host
./stops.py : Docker compose down for a host (does not remove volumes)
```
Run with no args to pick a host from a list, or `--host=name` to skip the prompt.

Each service can also have a `/task` folder (gen directories, fix permissions, backup, restore).\
Run them from the service's own directory `./task/data-set-permissions.sh`, not from inside `/task`.

---

## Komodo Notes

Komodo clones this repo into its own directory (`/etc/srv-kube`),
separate from wherever you're developing, never point it at your dev clone.
A deploy runs `git checkout -f` + `git pull --force`,
which wipes any uncommitted changes in whatever directory it's pointed at.

Commit and push before every deploy, Komodo only ever sees what's on `origin`.

---

## Wildcard Domains (Caddy)

If a host includes `caddy`, `./init.py` writes it a `caddyfile` at `host/<host-name>/caddyfile`.\
If it also includes `dnsmasq`, `./init.py` writes it a `dnsmasq.conf` the same way,
with a wildcard rule so `*.<host-name>` resolves to `127.0.0.1`,
and a `dnsmasq.sh` script that points your machine at it.

Which file actually gets mounted can be overridden per-host,
set `CADDY_CADDYFILE` / `DNSMASQ_CONF` in that host's `.env` to a path
relative to `serv/caddy` / `serv/dnsmasq`.\
Point it somewhere other than
that host's own auto-generated file to stop `./init.py` from touching it.

For those domains to actually resolve on your machine, run that script once,
on the machine, per host that has `dnsmasq` (needs `sudo`):
```
./host/<host-name>/dnsmasq.sh
```
It's rewritten on every `./init.py` run, re-run it if you add a host or the port changes.

---

## GPU-bound Services (llama.cpp, ComfyUI)

The `llama-cpp` and `comfyui` need direct GPU access (CUDA / Apple's Metal API), so on every host in this repo today they're installed straight onto the machine instead of through Docker.

This means `./start.py` and `./init.py` do **not** cover them, picking a host that "runs" one of these does not install, build, or start it, since neither is in that host's `docker-compose.yml` include list.

---

### `llama-cpp`

#### Requirements

| Requirement                                                    | Notes                                                                                                                        |
|----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| [Git](https://git-scm.com/download/win)                        |                                                                                                                              |
| [CMake](https://cmake.org/download/)                           |                                                                                                                              |
| [Visual Studio](https://visualstudio.microsoft.com/downloads/) | MSVC C/C++ build tools, the "Desktop development with C++" workload (Build Tools alone is enough, a full IDE isn't required) |

#### Setup: Linux / MacOS

```bash
        ./serv/llama-cpp/install.sh   # installation
python3 ./serv/llama-cpp/models.py    # downloads models listed in host/<host-name>/data/llama-cpp/models.yml
```

#### Setup: Windows

The `install.bat` needs the requirement tools, on `PATH`, installed by hand first.

Additionally `llama-cpp\install.bat` needs to run with the MSVC environment loaded, so `cl.exe` is on `PATH`, which a plain `cmd.exe`/PowerShell window doesn't set up on its own.
You can use on of these methods:
- Use the "Developer Command Prompt for VS" shortcut the Visual Studio installer adds to the Start Menu, `cd` into `serv\llama-cpp`, then run `install.bat`
- Load it and run the install in one line, from `cmd.exe`:
```cmd
cmd /k ""C:\Program Files\Microsoft Visual Studio\<edition>\VC\Auxiliary\Build\vcvarsall.bat" x64 && cd /d C:\path\to\srv-kube\serv\llama-cpp && install.bat"
```
- Load it and run the install in one line, from `powershell.exe`:
```powershell
cmd /c '"C:\Program Files\Microsoft Visual Studio\<edition>\VC\Auxiliary\Build\vcvarsall.bat" x64 && cd /d C:\path\to\srv-kube\serv\llama-cpp && install.bat'
```

> [!NOTE]
> The `<edition>` varies by Visual Studio install (example: `2022\BuildTools`, `2022\Community`). Find yours with:
>
> | Shell            | Command                                                                                                                                                                             |
> |------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> | `cmd.exe`        | `dir /s /b "C:\Program Files\Microsoft Visual Studio\vcvarsall.bat" "C:\Program Files (x86)\Microsoft Visual Studio\vcvarsall.bat"`                                                 |
> | `powershell.exe` | `(Get-ChildItem "C:\Program Files\Microsoft Visual Studio","C:\Program Files (x86)\Microsoft Visual Studio" -Recurse -Filter vcvarsall.bat -ErrorAction SilentlyContinue).FullName` |

> [!NOTE]
> On Windows, `install.bat` links `llama-server`/`llama-cli`/`llama` (and the `comfyui` wrapper) into `%USERPROFILE%\bin`, which isn't on `PATH` by default, so the plain `llama-server ...` / `comfyui ...` commands below won't resolve until you add it.
> 
> Do this once, then open a **new** terminal (PATH changes don't apply to an already-open session). `cmd.exe` shells out to PowerShell for the actual write, since `setx` alone risks silently truncating `PATH` past 1024 characters and corrupting it:
>
> | Shell            | Command                                                                                                                                                                             |
> |------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> | `cmd.exe`        | `powershell -NoProfile -Command "[Environment]::SetEnvironmentVariable('PATH', $([Environment]::GetEnvironmentVariable('PATH','User')) + ';' + $env:USERPROFILE + '\bin', 'User')"` |
> | `powershell.exe` | `[Environment]::SetEnvironmentVariable("PATH", "$([Environment]::GetEnvironmentVariable('PATH','User'));$env:USERPROFILE\bin", "User")`                                             |

#### Running Server

> [!NOTE]
> If `llama-server` exits immediately with no output at all (not even an error), that's `STATUS_DLL_NOT_FOUND` (exit code `-1073741515` / `0xC0000135`), not a bad model path. Unlike Linux, where a symlinked binary still finds its shared libraries through the build folder's own rpath, Windows looks for a DLL next to whatever path the exe was actually *invoked* from, so `llama.dll`/`ggml.dll`/`ggml-base.dll`/`ggml-cpu.dll`/`mtmd.dll`/`llama-common.dll`/`llama-server-impl.dll` all need to sit alongside the linked `llama-server.exe` in `%USERPROFILE%\bin`, not just in the build folder. `install.bat` links these in automatically now, but if you installed before this fix, copy them over by hand once:
>
> | Shell            | Command                                                                                                                  |
> |------------------|--------------------------------------------------------------------------------------------------------------------------|
> | `cmd.exe`        | `copy /Y "C:\path\to\srv-kube\serv\llama-cpp\code\build\bin\Release\*.dll" "%USERPROFILE%\bin\"`                         |
> | `powershell.exe` | `Copy-Item "C:\path\to\srv-kube\serv\llama-cpp\code\build\bin\Release\*.dll" -Destination "$env:USERPROFILE\bin" -Force` |

##### Commands: General

| Mode                            | Linux / MacOS                                                                                                                                                | Windows (cmd.exe)                                                                                                                                                                    | Windows (PowerShell)                                                                                                                                                                           |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Text-only                       | `llama-server --model ~/llms/models/llamacpp/<model>.gguf --host 0.0.0.0 --port 8080`                                                                        | `llama-server --model %USERPROFILE%\llms\models\llamacpp\<model>.gguf --host 0.0.0.0 --port 8080`                                                                                    | `llama-server --model "$env:USERPROFILE\llms\models\llamacpp\<model>.gguf" --host 0.0.0.0 --port 8080`                                                                                         |
| GPU offload + vision/file input | `llama-server --model ~/llms/models/llamacpp/<model>.gguf --mmproj ~/llms/models/llamacpp/<model-mmproj>.gguf --n-gpu-layers 999 --host 0.0.0.0 --port 8080` | `llama-server --model %USERPROFILE%\llms\models\llamacpp\<model>.gguf --mmproj %USERPROFILE%\llms\models\llamacpp\<model-mmproj>.gguf --n-gpu-layers 999 --host 0.0.0.0 --port 8080` | `llama-server --model "$env:USERPROFILE\llms\models\llamacpp\<model>.gguf" --mmproj "$env:USERPROFILE\llms\models\llamacpp\<model-mmproj>.gguf" --n-gpu-layers 999 --host 0.0.0.0 --port 8080` |

The GPU offload + vision/file input mode needs the model's own `--mmproj` file, some models ship one, e.g. `models.yml`'s `*-mmproj-f16.gguf` entries. Models live at `~/llms/models/llamacpp` (`%USERPROFILE%\llms\models\llamacpp` on Windows), that's where `models.py` downloads to. On Windows, note `cmd.exe` uses `%USERPROFILE%` while PowerShell needs `$env:USERPROFILE`, plain `%USERPROFILE%` is not expanded there and gets passed through as a literal, broken path.

##### Commands: Real example (Powershell)

```powershell
llama-server `
  --model "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-Q4_K_S.gguf" `
  --mmproj "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-mmproj-f16.gguf" `
  --n-gpu-layers 999 `
  --ctx-size 24576 `
  --host 0.0.0.0 `
  --port 8080 `
  --alias qwen3.5-9b `
  --flash-attn on
```

---

### `comfyui`

#### Requirements

| Requirement                                   | Notes                                       |
|-----------------------------------------------|---------------------------------------------|
| [Git](https://git-scm.com/download/win)       |                                             |
| [Python 3](https://www.python.org/downloads/) | check "Add python.exe to PATH" during setup |

#### Setup: Linux / MacOS

```bash
        ./serv/comfyui/install.sh     # installation
python3 ./serv/comfyui/models.py      # downloads models listed in host/<host-name>/data/comfyui/models.yml
```

#### Setup: Windows

The `install.bat` needs the requirement tools, on `PATH`, installed by hand first.

#### Running Server

Defaults to port `8188`

```bash
comfyui --listen 0.0.0.0
```

Models live at `~/llms/models/comfyui` (`%USERPROFILE%\llms\models\comfyui` on Windows), split into subfolders by category (checkpoints, loras, vae, etc.), matching ComfyUI's own `models/<category>` layout.

---

## Clean-up

Stopping services doesn't delete their data or config.
Most services store everything under `/serv/<service>/data`, remove it by hand to start fresh.
