---
name: explain-plain
description: Explain a named part of this codebase in full sentences, with a link for every code claim
argument-hint: [file, function or question]
disable-model-invocation: true
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Read the relevant code, then explain $ARGUMENTS in this order:

1. One sentence on what this part does and why the system needs it, with a link to where it starts.
2. Its inputs, its steps in the order they run, and its outputs. Give each step one or two sentences and a link.
3. One worked example with concrete values. Say whether the values came from running the code or are invented for illustration.
4. Definitions of any terms a newcomer would not know.
5. What you did not read, what you could not confirm, and the claim most likely to be wrong.
6. A section titled "Read the code in this order" with 3 to 5 links and, for each, one sentence on what to look for there.

Link every claim about code:
- Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory.
- Take line numbers from tool output, never from memory.
- If the logic lives outside this repository, do not invent a link. Write `NOT IN REPO:` followed by where it appears to live and the code that points to it.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with every location you plan to cite. Read each printed line, and correct any citation that does not show what your sentence says.

These examples show the voice I want. Match the voice, not the topic.

<example>Paste a short explanation you found clear. Use three to five varied samples.</example>
