---
name: pipeline-step
description: Explain one pipeline step using fixed fields for sources, logic, model input and output
argument-hint: [step name or number, and the pipeline]
disable-model-invocation: true
context: fork
background: false
disallowed-tools: Edit, Write
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Explain only this pipeline step, for a reader who knows nothing about its code, tables or terms: $ARGUMENTS

Use read-only commands, and use exactly these fields:

1. **Purpose:** why this step exists, in one or two sentences.
2. **Sources:** every input as an exact table.column or file path, with any filter applied and a link to the code.
3. **Logic:** a numbered list in execution order. Include every query, join and rule. For each rule, give the exact condition, the result, a link, and what happens when rules conflict.
4. **Model input:** if this step calls a model, name the model, then list every field or prompt section it receives and where each one comes from. Otherwise, write "no model".
5. **Output:** the exact destination, every column or field, and one example row.
6. **Example:** follow one real record through this step, showing its values before and after. Mask personal data.
7. **Unclear:** anything you could not confirm, or "nothing".

Writing rules:
- Use full, plain sentences, with no shorthand or compressed summaries.
- Define a term the first time you use it, and do not assume I already know anything.
- Use exact names from the code. Say "the table" only after you have named it.
- Mark each claim you did not directly confirm as "not verified".
- Do not suggest improvements.

Link format:
- Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory.
- Take line numbers from tool output, never from memory.
- If the logic lives outside this repository, do not invent a link. Write `NOT IN REPO:` followed by where it appears to live and the code that points to it.

Before you answer, run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check FILE:LINE FILE:LINE-LINE` with every location you plan to cite. Read each printed line, and correct any citation that does not show what your sentence says.
