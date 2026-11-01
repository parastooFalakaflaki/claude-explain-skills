---
name: test-status
description: Report how a pipeline or module is tested today and which parts have no test
argument-hint: [pipeline or module]
disable-model-invocation: true
context: fork
background: false
disallowed-tools: Edit, Write
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Report how this is tested today: $ARGUMENTS

Do not change anything, and do not print credentials or personal data. Use exactly these fields:

1. **Existing tests:** each test file with a link, what it checks in one sentence, and the command to run it.
2. **Latest result:** run the tests if that is safe and read-only, then give the pass and fail counts. If you cannot run them, say why.
3. **Data:** any labelled data or expected outputs, with exact locations and row counts.
4. **Quality checks:** any accuracy measures or data checks, and where they run.
5. **Not covered:** each step or rule with no test, with a link.
6. **Tests that may prove little:** tests that only repeat the code's current behaviour, or that would still pass if the logic broke, with links.

Report only what you confirmed, and mark everything else "not verified". Write full, plain sentences and define terms when you first use them. Do not write new tests or suggest a plan.

Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory. Take line numbers from tool output, never from memory.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with every location you plan to cite. Read each printed line, and correct any citation that does not show what your sentence says.
