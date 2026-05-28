# Manual Refactor Protocol

## Why this exists

We will not let an AI coding tool rewrite the whole app.

All Stage 2 changes must be small, controlled, testable, and reversible.

## Protocol

For every code change:

1. Identify exact file.
2. Identify exact section.
3. Copy only that section to ChatGPT.
4. Ask for exact replacement.
5. Paste into VS Code.
6. Save file.
7. Run Docker build.
8. Test browser.
9. Commit if successful.
10. Revert if broken.

## ChatGPT prompt template

```text
We are in Stage 2 — Code Stabilization for Sentinel.

Rules:
- no new features
- preserve current behavior
- no redesign
- no new tabs
- make the smallest safe change
- provide exact replacement code only
- explain where to paste it
- mention test command

File:
[paste file path]

Current code section:
[paste code]

Task:
[describe small cleanup/refactor]
```

## Unsafe tasks

Do not do these yet:

- rewrite full `page.tsx`
- redesign UI
- change API shape
- replace SQLite
- add OpenAI
- add authentication
- add PostgreSQL
- change Docker config without reason
