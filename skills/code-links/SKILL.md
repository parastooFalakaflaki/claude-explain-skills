---
name: code-links
description: Check the code links in a Markdown file and convert them to permanent web links
argument-hint: [path to Markdown file]
disable-model-invocation: true
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/codelink.py *)
---
Work on the file $ARGUMENTS. Do not change anything except its links.

1. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/codelink.py check --file $ARGUMENTS`.
2. Read the line printed under each citation and compare it with the sentence that cites it. Correct any citation that is broken or points to the wrong code. Read the file to find the right line.
3. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/codelink.py permalink $ARGUMENTS --write`.
4. Report how many links you checked, which you corrected, and any warning from the script. A link the script left local will not open for someone without this checkout.
