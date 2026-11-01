---
name: pipeline-trace
description: Trace one real record through the data pipeline, linking each stage to its code
argument-hint: [record id or sample input, and where the pipeline starts]
disable-model-invocation: true
context: fork
background: false
disallowed-tools: Edit, Write
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Trace $ARGUMENTS from its source to its final output. Use read-only commands.

For each stage, write full sentences that give:
- A link to the code that runs this stage, and a link to each rule or query it applies.
- The exact input and output values, copied from a command you ran.
- The row count before and after.

Mark anything you did not observe as INFERRED. If the record disappears, say at which stage and under which rule, and link to that rule.

Link format:
- Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory.
- Take line numbers from tool output, never from memory.
- If a stage runs from outside this repository, such as a warehouse scheduled query, do not invent a link. Write `NOT IN REPO:` followed by where it appears to live and the code that points to it.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with every location you plan to cite. Read each printed line, and correct any citation that does not show what your sentence says.

Do not write real customer values into any file. Define terms when you first use them. Aim for about 400 words, and go longer if the reader would otherwise lack what they need.

End with:
1. A section titled "Read the code in this order" with one link per stage.
2. What you did not read, what you could not confirm, and the three claims most likely to be wrong.
