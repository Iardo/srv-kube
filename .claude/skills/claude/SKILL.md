---
name: claude
description: Everything Claude related.
---

# Claude

These are formatting rules for Claude itself, not for the project.
Follow them whenever writing any explanation, anywhere, whatever the file or format.

## Rules

### Rules - General

- A `-` item must be a single line.
  - If a second, related line is needed, add it as a nested sub-item instead of a second line on the same item.
- A multi-line explanation must break onto a new line only at a comma or period, never in the middle of a phrase.
  - Aim to keep each line's length close to the others around it.
  - Let one line run longer than the rest when reaching the next comma or period at the target length would otherwise mean cutting a phrase mid-explanation.
  - A word and the punctuation that follows it, like "else," or "own.", must never be split across two lines, the break belongs right after that punctuation, not before it.
- An `Example:` line must be a sub-item of the rule it belongs to.
  - It must be the last sub-item under that rule.
- Explanations must be written in plain, everyday language, short but still clear about any technical requirement they cover.
  - Never use an em dash.
  - Do not overuse colons or parentheses, prefer commas and plain descriptive phrasing when a sentence needs to be split or a detail added.
- Explanatory text written as a sequence of short declarative lines that reads like a list of rules or facts must be converted into a proper bulleted list.
  - Apply the same formatting rules from this skill to that list.
- General rules and rules that only apply to one specific topic, like a single console, computer, or arcade board, must not sit mixed together in the same list.
  - Split them into a `### General Rules` header and a `### Specific Rules` header.
  - Under `### Specific Rules`, give each specific topic its own `#### Specific Rules: <topic>` header, following the header-grouping rule below, even when only one such topic exists yet.
  - Example: `#### Specific Rules: Windows` for rules that only apply to Windows, grouped under `### Specific Rules` alongside `### General Rules`.
- Headers that share an obvious topic must be grouped under one shared `###` header, with each grouped `####` title renamed to start with that shared term, a colon, then the rest of the title in the same plain sentence case already used elsewhere.
  - A header with no other header sharing its topic stays a standalone `####` under its `##` section, it does not get forced into a group of one.
  - Order every header alphabetically, both the top-level mix of standalone `####` headers and `###` group headers under their `##` section, and the grouped `####` titles within each `###` group.
  - Example: `Setup: Linux` and `Setup: Windows`, grouped under `### Setup`.
- Items at the same list level must be ordered alphabetically.
  - This includes top-level `-` items and nested sub-items.
  - The only exception is an `Example:` sub-item, which always goes last regardless of alphabetical order.

### Rules - Code

- A comment or docstring must not restate what a name, a class's structure, or its place next to identical siblings already makes obvious.
  - Only write one when it adds something the reader could not already tell, like a gotcha, an edge case, or a rule a name alone would not carry.
  - When nothing like that exists, write no comment or docstring at all rather than restating the name.
  - Example: a `Cat` class sitting next to a `Dog` class and a `Bird` class, each under an `Animals` class, does not need the docstring `Handles everything about a cat.`, its name and its place next to those siblings already say that.
- A name built from a shared, general term and one or more specific qualifiers must put the general term first, not the qualifier.
  - This groups every name that shares that general term together, both alphabetically and visually, instead of scattering them wherever their own qualifier happens to start.
  - Applies to constants, config keys, `.env` variables, and any other name built the same way.
  - Example: `TOKEN_URL` becomes `URL_TOKEN`, and `API_URL` becomes `URL_API`, so every `URL_*` name for one thing sits together.
