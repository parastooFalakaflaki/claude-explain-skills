---
name: explain-why
description: Explain why a rule or piece of logic exists, what depends on it, and whether the reason is known
argument-hint: [rule, condition, file or function]
disable-model-invocation: true
context: fork
background: false
disallowed-tools: Edit, Write
allowed-tools: Bash(git log *) Bash(git blame *) Bash(git show *) Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Explain why this logic exists, for a reader who did not write it: $ARGUMENTS

Read the code, then check its git history with `git log` and `git blame`. Do not change anything. Use exactly these fields:

1. **What it does:** the exact condition and result in plain sentences, with a link.
2. **Why it exists:** the reason, with its evidence, such as a commit message, a comment or a test. If you find no evidence, write "reason unknown" and do not guess.
3. **What depends on it:** the code or outputs that use its result, with links.
4. **If removed:** what would change, and whether you confirmed that or are inferring it.
5. **When it was added:** the commit and date, and whether the commit message explains it.
6. **Unclear:** anything you could not confirm, or "nothing".

If the reason is unknown and nothing appears to depend on it, say so plainly, because this logic is a candidate to question or cut. Do not recommend anything beyond that.

Write full, plain sentences and define terms when you first use them.

Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory. Take line numbers from tool output, never from memory.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with every location you plan to cite. Read each printed line, and correct any citation that does not show what your sentence says.
