---
name: check-my-understanding
description: Test my understanding of a pipeline stage, linking each correction to the code
argument-hint: [socratic | teach-back | predict] [module or flow]
disable-model-invocation: true
disallowed-tools: Edit, Write
---
The mode and target are: $ARGUMENTS

socratic: Do not explain yet. Ask me one question at a time, starting from my notes. If a question needs me to read code, link to it. Correct me only after I answer, and link to the code behind each correction.

teach-back: I will explain the flow in my own words. List what I got wrong and what I left out, with a link to the code behind each point. Do not praise me or rewrite my explanation.

predict: Give me five inputs, including edge cases, and hide the outputs. I will predict the outputs, then we will run the code and compare. For each wrong prediction, link to the line that decided the result.

Use `[path/to/file.py:42](path/to/file.py:42)` for a line and `[path/to/file.py:60-85](path/to/file.py:60)` for a block, with paths relative to the current working directory. Take line numbers from tool output, never from memory.
