---
name: pipeline-map
description: List every step of a pipeline that actually runs, with its code, inputs and outputs
argument-hint: [pipeline name or entry point]
disable-model-invocation: true
context: fork
background: false
disallowed-tools: Edit, Write
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Map this pipeline for a reader who knows nothing about its code, tables or terms: $ARGUMENTS

Find the path that actually runs in production, starting from the scheduled job or entry point. Say how you confirmed that it runs, or write "not verified". Use read-only commands.

Give a numbered list of steps. For each step, give only these fields:
- **Name:** what the step is called in the code.
- **Does:** one plain sentence saying what it does.
- **Code:** a link to where it runs.
- **Reads:** the exact table, file or API.
- **Writes:** the exact table, file or API.

Then give:
- **Terms:** each term a newcomer would not know, with a one-line definition.
- **Not in the path:** code that looks old or unused, with links. Do not explain it.
- **Unclear:** anything you could not confirm.

Link format:
- Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory.
- Take line numbers from tool output, never from memory.
- If a step runs from outside this repository, such as a warehouse scheduled query, do not invent a link. Write `NOT IN REPO:` followed by where it appears to live and the code that points to it.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with every location you plan to cite. Read each printed line, and correct any citation that does not show what your sentence says.

Write full, plain sentences with no shorthand. Do not suggest improvements. End by telling me to run `/pipeline-step` on the step I want to understand.
