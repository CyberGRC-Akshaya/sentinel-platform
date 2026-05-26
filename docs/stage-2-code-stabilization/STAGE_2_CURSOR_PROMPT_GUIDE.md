# Stage 2 Cursor Prompt Guide

Use Cursor carefully. Do not ask Cursor to rewrite the whole app.

## Golden prompt rule

Always say:

- preserve behavior
- no new features
- one file/module at a time
- explain changed files
- do not redesign UI
- run/build check after change

## Start with analysis prompt

Use the prompt in:

```text
cursor-prompts/STAGE_2_CODEBASE_ANALYSIS_PROMPT.md
```

## Then refactor frontend

Use:

```text
cursor-prompts/STAGE_2_FRONTEND_SAFE_REFACTOR_PROMPT.md
```

## Then refactor backend

Use:

```text
cursor-prompts/STAGE_2_BACKEND_SAFE_REFACTOR_PROMPT.md
```
