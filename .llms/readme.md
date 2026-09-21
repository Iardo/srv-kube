# LLM Config

This folder is the one real copy of every rule, skill, and script that LLMs coding agents use in this repo.

## Why `.llms/`

Different tools look for this content in different places.
Keeping two separate copies would drift out of sync, so instead the other tools configuration folders are junctions (Windows) or symlinks (Linux/macOS) pointing back at this folder, and the root configurations are a hardlink to `.llms/AGENTS.md`. Edit a file once, in here, and every tool sees the change.

## Folders

| Folder        | What it's for                                                                                        |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| `memory/`     | Reserved for future use, empty for now                                                               |
| `references/` | Reserved for future use, empty for now                                                               |
| `rules/`      | Instructions loaded into every task automatically, any `.md` file here counts                        |
| `scripts/`    | Reserved for future use, empty for now                                                               |
| `skills/`     | Reference docs an agent reads on demand, when a task touches the area it covers, see the table below |
| `workflows/`  | Reserved for future use, empty for now                                                               |

## Setup

After cloning this repo, run one of these once to create the links and the root `CLAUDE.md` link:

```bash
.llms/linkdirs.sh    # Linux/MacOS
.llms/linkdirs.bat   # Windows
```

Safe to re-run any time, for example if a link ever gets deleted by accident.

## Available Skills

| Skill                                         | What it covers                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------ |
| `.llms/skills/local-integrations/SKILL.md`    | External tools/editors that integrate with this project's services             |
| `.llms/skills/local-services/SKILL.md`        | How services deploy across hosts, and the GPU-bound native-install exception   |
