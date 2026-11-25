---
name: local-integrations
description: Everything about external tools and editors that integrate with this project's services.
---

# Local Integrations

- An "integration" is an external application or editor extension that connects to one of this project's services, not a service in this repo itself
- A failure while using an integration is not automatically the service's fault, check the integration's own logs and config before assuming a service like `llama-cpp` or `comfyui` is broken

## General Rules

- Treat an integration's own console/output panel as the first thing to check on a hang or error, before touching the service it's talking to
  - Example: RooCode logging `ripgrep not found: undefined` looks alarming next to a stuck request, and can genuinely be the cause, check Specialized Rules: VSCode: Extension: RooCode below before assuming `llama-server` is broken

## Specialized Rules

### Specialized Rules: VSCode

- VS Code ships its own bundled ripgrep binary, at `<VS Code install>\resources\app\node_modules.asar.unpacked\@vscode\ripgrep-universal\bin\win32-x64\rg.exe`, but that folder is not on `PATH` by default
  - Any extension that shells out to `rg`/`ripgrep` for its own search features fails with something like `ripgrep not found: undefined` until that folder is added to `PATH`
  - Add it with `[Environment]::SetEnvironmentVariable(...)`, the same `PATH`-safe approach as `%USERPROFILE%\bin` in the `local-services` skill's Specialized Rules: Operating Systems: Windows, then restart VS Code, see `docs/services-gpu-bound.md`'s Integrations section for the exact commands
- `<VS Code install>` includes a build-hash folder segment (e.g. `645f29cc31`) that changes on every VS Code update, so a `PATH` entry copied from a previous version breaks silently after updating, re-locate `rg.exe` with `Get-ChildItem` instead of hardcoding a hash seen once

#### Extension: RooCode

- A hang on a simple prompt with the ripgrep hardlink fix below already applied is not explained by ripgrep, look at `llama-server`'s own logs and RooCode's model/provider settings (endpoint, context size matching the model's chat template) instead
- RooCode can point at a locally running `llama-server` as its model provider instead of a cloud API
- RooCode's own ripgrep lookup ignores `PATH` entirely, it only checks a few hardcoded paths under VS Code's own install folder, one of which is `node_modules.asar.unpacked\@vscode\ripgrep\bin\rg.exe`, so the general VSCode `PATH` fix above does not fix RooCode even though it fixes other extensions
  - Fix it by hardlinking `rg.exe` into the path RooCode expects, see `docs/services-gpu-bound.md`'s Integrations section for the exact commands, safe to re-run, and needs re-running after a VS Code update wipes the link
  - Newer VS Code builds ship that binary under a renamed, restructured `@vscode\ripgrep-universal\bin\win32-x64\rg.exe` package instead, which none of RooCode's hardcoded paths match
  - RooCode also uses `rg` to list workspace files for every request's context, not just its codebase-search feature, so this failure can throw before RooCode ever builds the request, looking exactly like a hang that never reaches `llama-server` at all
