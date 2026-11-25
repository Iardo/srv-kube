# GPU-bound Services (llama.cpp, ComfyUI)

The `llama-cpp` and `comfyui` need direct GPU access (CUDA / Apple's Metal API), so on every host in this repo today they're installed straight onto the machine instead of through Docker.

This means `./start.py` and `./init.py` do **not** cover them, picking a host that "runs" one of these does not install, build, or start it, since neither is in that host's `docker-compose.yml` include list.

---

## `llama-cpp`

### Requirements

| Requirement                                                      | Notes                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)      | Only for NVIDIA GPU offload, the driver alone (what `nvidia-smi` reports) isn't enough, `install.bat` needs `nvcc` on `PATH` or it silently builds CPU-only                                                                                                                                                   |
| [FFmpeg](https://ffbinaries.com/downloads)                       | Only for `.webp` image input, llama.cpp's built-in image decoder (`stb_image`) doesn't support `.webp` and falls back to `ffmpeg`/`ffprobe` to decode it as a single video frame, without it that image is silently dropped from the request instead of erroring loudly                                       |
| [FFprobe](https://git-scm.com/download/win)                      | Only for `.webp` image input, llama.cpp's built-in image decoder (`stb_image`) doesn't support `.webp` and falls back to `ffmpeg`/`ffprobe` to decode it as a single video frame, without it that image is silently dropped from the request instead of erroring loudly                                       |
| [Git](https://git-scm.com/download/win)                          |                                                                                                                                                                                                                                                                                                               |
| [CMake](https://cmake.org/download/)                             |                                                                                                                                                                                                                                                                                                               |
| [Visual Studio](https://visualstudio.microsoft.com/downloads/)   | MSVC C/C++ build tools, the "Desktop development with C++" workload (Build Tools alone is enough, a full IDE isn't required)                                                                                                                                                                                  |

### Setup: Linux / MacOS

```bash
        ./serv/llama-cpp/install.sh   # installation
python3 ./serv/llama-cpp/models.py    # downloads models listed in host/<host-name>/data/llama-cpp/models.yml
```

### Setup: Windows

The `install.bat` needs the requirement tools, on `PATH`, installed by hand first.

Additionally `llama-cpp\install.bat` needs to run with the MSVC environment loaded, so `cl.exe` is on `PATH`, which a plain `cmd.exe`/PowerShell window doesn't set up on its own.
You can use on of these methods:
1. Use the "Developer Command Prompt for VS" shortcut the Visual Studio installer adds to the Start Menu
  - run `cd` into `serv\llama-cpp`
  - run `install.bat`
2. From the repo root, run the install in one line
  - auto-locates `vcvarsall.bat` instead of hardcoding which Visual Studio edition/year you have installed
  - auto-locates `serv\llama-cpp` off your current directory instead of a hardcoded repo path

| Shell            | Command                                                                                                                                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cmd.exe`        | `for /f "delims=" %i in ('dir /s /b "C:\Program Files\Microsoft Visual Studio\vcvarsall.bat" "C:\Program Files (x86)\Microsoft Visual Studio\vcvarsall.bat" 2^>nul') do cmd /k ""%i" x64 && cd /d %CD%\serv\llama-cpp && install.bat"`                                   |
| `powershell.exe` | `cmd /c ('"' + (Get-ChildItem "C:\Program Files\Microsoft Visual Studio","C:\Program Files (x86)\Microsoft Visual Studio" -Recurse -Filter vcvarsall.bat -ErrorAction SilentlyContinue)[0].FullName + '" x64 && cd /d ' + $PWD.Path + '\serv\llama-cpp && install.bat')` |

> [!NOTE]
> On Windows, `install.bat` links `llama-server`/`llama-cli`/`llama` (and the `comfyui` wrapper) into `%USERPROFILE%\bin`, which isn't on `PATH` by default, so the plain `llama-server ...` / `comfyui ...` commands below won't resolve until you add it.
> 
> Do this once, then open a **new** terminal (PATH changes don't apply to an already-open session). `cmd.exe` shells out to PowerShell for the actual write, since `setx` alone risks silently truncating `PATH` past 1024 characters and corrupting it:
>
> | Shell              | Command                                                                                                                                                                               |
> | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `cmd.exe`          | `powershell -NoProfile -Command "[Environment]::SetEnvironmentVariable('PATH', $([Environment]::GetEnvironmentVariable('PATH','User')) + ';' + $env:USERPROFILE + '\bin', 'User')"`   |
> | `powershell.exe`   | `[Environment]::SetEnvironmentVariable("PATH", "$([Environment]::GetEnvironmentVariable('PATH','User'));$env:USERPROFILE\bin", "User")`                                               |

### Running Server

> [!NOTE]
> `failed to launch ffprobe` followed by `failed to decode webp buffer` means FFmpeg (see Requirements above) isn't installed, install it then open a **new** terminal so `PATH` picks it up:
> ```
> winget install --id Gyan.FFmpeg --source winget
> ```

> [!NOTE]
> If `llama-server` exits immediately with no output at all (not even an error), that's `STATUS_DLL_NOT_FOUND` (exit code `-1073741515` / `0xC0000135`), not a bad model path. Unlike Linux, where a symlinked binary still finds its shared libraries through the build folder's own rpath, Windows looks for a DLL next to whatever path the exe was actually *invoked* from, so `llama.dll`/`ggml.dll`/`ggml-base.dll`/`ggml-cpu.dll`/`mtmd.dll`/`llama-common.dll`/`llama-server-impl.dll` all need to sit alongside the linked `llama-server.exe` in `%USERPROFILE%\bin`, not just in the build folder. `install.bat` links these in automatically now, but if you installed before this fix, copy them over by hand once:
>
> | Shell              | Command                                                                                                                    |
> | ------------------ | -------------------------------------------------------------------------------------------------------------------------- |
> | `cmd.exe`          | `copy /Y "C:\path\to\srv-kube\serv\llama-cpp\code\build\bin\Release\*.dll" "%USERPROFILE%\bin\"`                           |
> | `powershell.exe`   | `Copy-Item "C:\path\to\srv-kube\serv\llama-cpp\code\build\bin\Release\*.dll" -Destination "$env:USERPROFILE\bin" -Force`   |

> [!NOTE]
> `install.bat` only builds with GPU offload if `nvcc` (the CUDA Toolkit's compiler, not just the driver) was on `PATH` at build time, otherwise it prints a warning and silently builds CPU-only, `--n-gpu-layers` then does nothing even though `nvidia-smi` reports the GPU fine. The clearest sign is `llama-server`'s own startup log: a CPU-only build prints `warning: no usable GPU found, --gpu-layers option will be ignored` right after `initializing ...`, a working GPU build doesn't. Other symptoms: GPU usage stays near idle during generation, RAM usage matches the model file size instead of VRAM usage, and prompt processing throughput sits around 90 tokens/sec on a 9B model regardless of GPU, instead of the thousands a card like an RTX 5070 should give (measured on this project: ~85 tokens/sec CPU-only vs. ~3,600 tokens/sec once GPU offload was fixed, a ~40x difference, generation throughput went from ~9 to ~94 tokens/sec, ~10x). You can also check which build you have directly, from the repo root:
>
> | Shell            | Command                                                                                                       |
> | ---------------- | ------------------------------------------------------------------------------------------------------------- |
> | `cmd.exe`        | `findstr "GGML_CUDA:BOOL" "%CD%\serv\llama-cpp\code\build\CMakeCache.txt"`                                    |
> | `powershell.exe` | `Select-String -Path "$PWD\serv\llama-cpp\code\build\CMakeCache.txt" -Pattern "GGML_CUDA:BOOL"`               |
>
> If that reads `GGML_CUDA:BOOL=OFF`, install the CUDA Toolkit, open a **new** terminal so `nvcc` is on `PATH`, then force a rebuild, from the repo root:
>
> | Shell            | Command                                                                     |
> | ---------------- | --------------------------------------------------------------------------- |
> | `cmd.exe`        | `del "%CD%\serv\llama-cpp\code\.installed"`                                 |
> | `powershell.exe` | `Remove-Item "$PWD\serv\llama-cpp\code\.installed"`                         |
>
> then re-run the "Setup: Windows" one-liner above, it re-detects `nvcc` and rebuilds with `-DGGML_CUDA=ON`.

#### Commands: General

| Mode                              | Linux / MacOS                                                                                                                                                  | Windows (cmd.exe)                                                                                                                                                                      | Windows (PowerShell)                                                                                                                                                                             |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Text-only                         | `llama-server --model ~/llms/models/llamacpp/<model>.gguf --host 0.0.0.0 --port 8080`                                                                          | `llama-server --model %USERPROFILE%\llms\models\llamacpp\<model>.gguf --host 0.0.0.0 --port 8080`                                                                                      | `llama-server --model "$env:USERPROFILE\llms\models\llamacpp\<model>.gguf" --host 0.0.0.0 --port 8080`                                                                                           |
| GPU offload + vision/file input   | `llama-server --model ~/llms/models/llamacpp/<model>.gguf --mmproj ~/llms/models/llamacpp/<model-mmproj>.gguf --n-gpu-layers 999 --host 0.0.0.0 --port 8080`   | `llama-server --model %USERPROFILE%\llms\models\llamacpp\<model>.gguf --mmproj %USERPROFILE%\llms\models\llamacpp\<model-mmproj>.gguf --n-gpu-layers 999 --host 0.0.0.0 --port 8080`   | `llama-server --model "$env:USERPROFILE\llms\models\llamacpp\<model>.gguf" --mmproj "$env:USERPROFILE\llms\models\llamacpp\<model-mmproj>.gguf" --n-gpu-layers 999 --host 0.0.0.0 --port 8080`   |

The GPU offload + vision/file input mode needs the model's own `--mmproj` file, some models ship one, e.g. `models.yml`'s `*-mmproj-f16.gguf` entries. Models live at `~/llms/models/llamacpp` (`%USERPROFILE%\llms\models\llamacpp` on Windows), that's where `models.py` downloads to. On Windows, note `cmd.exe` uses `%USERPROFILE%` while PowerShell needs `$env:USERPROFILE`, plain `%USERPROFILE%` is not expanded there and gets passed through as a literal, broken path.

#### Commands: Real example (Powershell)

##### One-liner
```powershell
llama-server --model "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-Q4_K_S.gguf" --mmproj "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-mmproj-f16.gguf" --alias qwen3.5-9b --port 8080 --host 0.0.0.0 --ctx-size 49152 --parallel 1 --n-gpu-layers 999 --jinja --flash-attn on
```

##### Multi-line
```powershell
llama-server `
  --model "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-Q4_K_S.gguf" `
  --mmproj "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-mmproj-f16.gguf" `
  --alias qwen3.5-9b `
  --port 8080 `
  --host 0.0.0.0 `
  --ctx-size 49152 `
  --parallel 1 `
  --n-gpu-layers 999 `
  --jinja `
  --flash-attn on
```

`--parallel 1` matches how RooCode (and most single-conversation clients) actually use the server, one request at a time, without it the default of 4 slots each reserve their own KV cache sized to the full context, wasting VRAM on parallelism nothing is using instead of letting it go toward a larger usable context.

---

## `comfyui`

### Requirements

| Requirement                                     | Notes                                         |
| ----------------------------------------------- | --------------------------------------------- |
| [Git](https://git-scm.com/download/win)         |                                               |
| [Python 3](https://www.python.org/downloads/)   | check "Add python.exe to PATH" during setup   |

### Setup: Linux / MacOS

```bash
        ./serv/comfyui/install.sh     # installation
python3 ./serv/comfyui/models.py      # downloads models listed in host/<host-name>/data/comfyui/models.yml
```

### Setup: Windows

The `install.bat` needs the requirement tools, on `PATH`, installed by hand first.

### Running Server

Defaults to port `8188`

```bash
comfyui --listen 0.0.0.0
```

Models live at `~/llms/models/comfyui` (`%USERPROFILE%\llms\models\comfyui` on Windows), split into subfolders by category (checkpoints, loras, vae, etc.), matching ComfyUI's own `models/<category>` layout.

---

## Integrations

### VSCode: RooCode

RooCode (and similar AI coding extensions) can point at a locally running `llama-server` as its model provider instead of a cloud API, but the extension's own tooling can fail independently of the model connection itself, don't assume a stuck or hung request is `llama-server`'s fault before checking the extension's own console.

An easy-to-hit failure: RooCode's Output panel (`Roo-Code` channel) may show `ripgrep not found: undefined`, this is RooCode failing to find `rg`, not a problem with `llama-server` or the model, though as the note below explains it can escalate into a full hang, not just broken codebase search. VS Code ships its own bundled ripgrep, but it's not on `PATH` by default, and its install path includes a build-hash folder segment (e.g. `645f29cc31`) that changes on every VS Code update, so it needs to be located rather than hardcoded:

| Shell              | Command                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `powershell.exe`   | `$rg = (Get-ChildItem "$env:LOCALAPPDATA\Programs\Microsoft VS Code\*\resources\app\node_modules.asar.unpacked\@vscode\ripgrep-universal\bin\win32-x64\rg.exe" -ErrorAction SilentlyContinue)[0].DirectoryName; [Environment]::SetEnvironmentVariable("PATH", "$([Environment]::GetEnvironmentVariable('PATH','User'));$rg", "User")`                                     |
| `cmd.exe`          | `powershell -NoProfile -Command "$rg = (Get-ChildItem '%LOCALAPPDATA%\Programs\Microsoft VS Code\*\resources\app\node_modules.asar.unpacked\@vscode\ripgrep-universal\bin\win32-x64\rg.exe' -ErrorAction SilentlyContinue)[0].DirectoryName; [Environment]::SetEnvironmentVariable('PATH', $([Environment]::GetEnvironmentVariable('PATH','User')) + ';' + $rg, 'User')"` |

Restart VS Code once that's set, `PATH` changes don't apply to an already-open session.

> [!NOTE]
> If VS Code is installed system-wide instead of per-user, look under `C:\Program Files\Microsoft VS Code` instead of `$env:LOCALAPPDATA\Programs\Microsoft VS Code`.

#### If RooCode Still Reports `ripgrep not found` After That

RooCode doesn't actually check `PATH` for `rg`, it only looks for a `rg.exe` at a few fixed locations under VS Code's own install folder, one of which is `node_modules.asar.unpacked\@vscode\ripgrep\bin\rg.exe`. Newer VS Code builds ship that binary under a renamed, restructured package instead, `@vscode\ripgrep-universal\bin\win32-x64\rg.exe`, which none of RooCode's fixed locations match, so the `PATH` fix above does nothing for it and it keeps failing.

This isn't just RooCode's codebase-search feature failing gracefully, it also uses `rg` to list workspace files for every request's context, and that call can throw before RooCode ever builds the request, which looks exactly like a hung "hello" that never reaches `llama-server` at all.

The fix is to hardlink `rg.exe` into the old path RooCode expects, pointing at the real binary VS Code actually ships:

| Shell            | Command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `powershell.exe` | `$rg = (Get-ChildItem "$env:LOCALAPPDATA\Programs\Microsoft VS Code\*\resources\app\node_modules.asar.unpacked\@vscode\ripgrep-universal\bin\win32-x64\rg.exe" -ErrorAction SilentlyContinue)[0].FullName; $dest = $rg -replace 'ripgrep-universal\\bin\\win32-x64\\rg\.exe$','ripgrep\bin\rg.exe'; New-Item -ItemType Directory -Force -Path (Split-Path $dest) \| Out-Null; if (-not (Test-Path $dest)) { New-Item -ItemType HardLink -Path $dest -Target $rg \| Out-Null }`                               |
| `cmd.exe`        | `powershell -NoProfile -Command "$rg = (Get-ChildItem '%LOCALAPPDATA%\Programs\Microsoft VS Code\*\resources\app\node_modules.asar.unpacked\@vscode\ripgrep-universal\bin\win32-x64\rg.exe' -ErrorAction SilentlyContinue)[0].FullName; $dest = $rg -replace 'ripgrep-universal\\bin\\win32-x64\\rg\.exe$','ripgrep\bin\rg.exe'; New-Item -ItemType Directory -Force -Path (Split-Path $dest) \| Out-Null; if (-not (Test-Path $dest)) { New-Item -ItemType HardLink -Path $dest -Target $rg \| Out-Null }"` |

It's safe to re-run, it skips the link if it already exists. Restart VS Code afterward.

> [!NOTE]
> A VS Code update replaces the whole `node_modules.asar.unpacked` folder (and its build-hash segment), which wipes this hardlink, re-run the command above after every VS Code update if RooCode starts hanging again.

#### Why The First Message Can Still Take Minutes

Even with ripgrep fixed, RooCode sends its full system prompt, tool definitions, mode instructions, and a workspace file listing, on every request, no matter how short your actual message is. A first "hello" in a fresh task can easily run 10,000+ tokens once that's all included, confirmed from this project's own RooCode logs (`api_conversation_history.json`/`ui_messages.json` under `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\tasks\<task-id>`), where a 10,411-token prompt took about 128 seconds to process before the first reply token appeared, with nothing in RooCode's UI to say it was still working.

That number came from a build without working GPU offload (see the `llama-cpp` Running Server section's CUDA note above), where prompt processing ran at only ~85 tokens/sec. Fixing GPU offload on this same host confirmed the fix: prompt processing jumped to ~3,600 tokens/sec, which would cut that same 10,411-token prompt down to about 3 seconds. Either way, treat a silent wait on the very first message of a task as expected, not a hang, RooCode gives no progress indicator for it, how long it takes just depends on whether GPU offload is actually working.
