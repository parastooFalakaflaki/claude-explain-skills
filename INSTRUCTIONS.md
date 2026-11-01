# Instructions for the model installing this repository

This repository contains personal Claude Code skills that make explanations of a codebase clear and link each claim to the code. Follow these steps when the user asks you to install or update it. Everything installs into `~/.claude`, so it does not change any project repository.

## Install

1. Read `install.sh` and `skills/code-links/scripts/codelink.py` before running anything. The installer only copies files, and the script uses the Python standard library and local git commands. If either file does something else, stop and tell the user.
2. Confirm that `python3` and `git` are available.
3. Run `bash install.sh` from this repository's root. If it lists files that already exist, nothing has been copied. Show the user what differs with `diff -ru`, and run `bash install.sh --force` only after they approve.
4. Set the output style in `~/.claude/settings.json` by adding `"outputStyle": "Plain explainer"`.
   - Keep every other setting in the file. Create the file if it does not exist.
   - If `outputStyle` is already set to something else, ask the user before changing it.
   - The value is case-sensitive, and a wrong value silently gives the default style.
   - A project's `.claude/settings.json` or `.claude/settings.local.json` overrides this value, so tell the user if the current project sets one.
5. Tell the user to restart Claude Code, then to run this as the first test, using a real question about their code:

   ```text
   /where-is how the final rejection reason gets chosen
   ```

## Tell the user how to call the skills

Every skill except the style has `disable-model-invocation: true`, so only the user can start one, by typing its command. You cannot call them yourself. When one would help, name the command and let the user run it.

| Command | Use it to |
|---|---|
| `/where-is [behaviour]` | Get up to 8 links to the code behind a behaviour, with no explanation |
| `/explain-plain [file, function or question]` | Get a full explanation with links and a suggested reading order |
| `/pipeline-trace [record and starting point]` | Follow one real record through the pipeline using real command output |
| `/check-my-understanding [socratic, teach-back or predict] [target]` | Be tested on a part of the code |
| `/pipeline-dossier [pipeline name and output file]` | Write a checked record of the pipeline with permanent links |
| `/code-links [Markdown file]` | Check the links in a file and make them permanent |

The `independent-reader` subagent gives a second answer from the code. Give it the question and not the first answer.

## Finish setup

`explain-plain` contains a placeholder `<example>` block. Ask the user for three to five explanations they found clear, and replace the placeholder in `~/.claude/skills/explain-plain/SKILL.md`. If they have none yet, delete the placeholder block.

## Keep company material out of this repository

This repository is on the user's personal GitHub account. Never commit company code, data, table names, pipeline details or writing samples to it. Those belong only in the installed copies under `~/.claude` or in the work repository. Changes to the skills themselves must stay generic.

## Update

1. Run `git pull` in this repository.
2. Copy the user's `<example>` blocks out of `~/.claude/skills/explain-plain/SKILL.md`, because the next step replaces that file.
3. Run `bash install.sh --force`, then put the examples back.
4. Tell the user to restart Claude Code.

## Known limits

- The link checker and installer were tested on a small sample repository. The skills had not been run end to end in Claude Code when this was written, so report anything that fails on first use.
- If Claude Code asks permission to run `codelink.py` inside `/where-is` or `/pipeline-trace`, the user can approve it. If the skill cannot run the script, it should read the cited lines itself and say the check did not run.
- `where-is` uses `model: haiku` to save tokens. If its results miss important code, change that line to `model: sonnet`. If the organisation does not allow the named model, the skill uses the session's model.
- The checker proves that a cited line exists and shows it. It does not prove that the claim about that line is correct.
- `disallowed-tools` does not stop Bash from writing, so `/pipeline-trace` needs read-only database credentials.
- Links in chat open the local copy, and some terminals open the file without jumping to the line. The visible path and line number are the fallback.
