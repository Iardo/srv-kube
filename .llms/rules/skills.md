# Project Skills

This repo keeps its own rules and reference material under `.llms/skills/`, shared by every tool through a junction, read the relevant file with `read_file` when it applies, none of them are preloaded into this prompt.

Read whichever of these covers the area a task touches, before starting on it:

| Skill file                                   | What it covers                                                                |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| `.llms/skills/local-integrations/SKILL.md`   | External tools/editors that integrate with this project's services            |
| `.llms/skills/local-services/SKILL.md`       | How services deploy across hosts, and the GPU-bound native-install exception  |
