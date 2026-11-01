---
name: clearer
description: Rewrite a confusing part of the last answer using exact names and plain sentences
argument-hint: [the sentence or part you did not understand]
disable-model-invocation: true
---
This part of your last answer was unclear: $ARGUMENTS

Rewrite only that part, in the same length or slightly longer. Do not repeat the rest of the answer, and do not apologise or explain what went wrong.

- Replace every vague word, such as "it", "this" or "the layer", with the exact table, function, condition or file it refers to.
- Add a link for each claim about code, using `[path/to/file.py:42](path/to/file.py:42)`, with line numbers from tool output.
- Use full sentences, and define any term I would not know.
- If you cannot make it exact because you did not confirm it, say that plainly.
