---
name: where-is
description: Find the code behind a behaviour and answer with links only, no explanation
argument-hint: [behaviour or question]
disable-model-invocation: true
context: fork
agent: Explore
model: haiku
background: false
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Find the code in this repository that is responsible for: $ARGUMENTS

Search the code and read only enough to be sure of each location. Do not change anything.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with your locations. Read each printed line, and drop or correct any location that does not show what you are about to claim.

Answer with this list and nothing before it. Put the locations in the order the code runs, and use at most 8.

- [path/to/file.py:42](path/to/file.py:42): One full sentence saying what the reader will see at that line.
- [path/to/file.py:60-85](path/to/file.py:60): For a block, show the range in the label and open the link at its first line.

Rules:
- Write paths relative to the current working directory, exactly as your tools report them.
- Take line numbers from tool output, never from memory.
- If the logic lives outside this repository, such as a warehouse scheduled query or a dashboard, do not invent a link. Write `NOT IN REPO:` followed by where it appears to live and the code that points to it.
- If you found nothing, say so and list what you searched for.

End with one line starting `Start here:` that names the single link to open first.
