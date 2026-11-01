---
name: pipeline-dossier
description: Write a short record of the pipeline from checks that were run, with permanent code links
argument-hint: [pipeline name and output file path]
disable-model-invocation: true
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py *)
---
Write a record of the pipeline described by: $ARGUMENTS

Include only facts you checked by reading the code or running a read-only command. Put everything else under "Unknown". Do not write real customer values into the file.

Use these sections:
- **Sources:** each table or API, its owner, refresh time, and row count from a query.
- **Lineage:** each output column, its inputs, and how it is transformed.
- **Rules:** an ID, a plain statement, the reason, a link to the code, and one input with its expected output. Write "reason unknown" if the code and history do not show it.
- **Model step:** the pinned model ID, prompt version, input fields, labels and failure handling, with links. Write "no model" if there is none.
- **Outputs:** the destination, its consumers, and any thresholds.
- **Evidence:** the command behind each checked claim, and today's date.
- **Unknown:** everything you could not confirm.

While drafting, link with `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory. Take line numbers from tool output. For logic outside this repository, write `NOT IN REPO:` and where it appears to live.

After you save the file:
1. Run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py check --file OUTPUT_FILE`. Read each printed line and correct anything that does not match its claim.
2. Run `python3 ${CLAUDE_SKILL_DIR}/../code-links/scripts/codelink.py permalink OUTPUT_FILE --write`, so the links keep pointing at this version after the code changes.
3. Report the file path, the commit the links point to, and any link the script left local.
