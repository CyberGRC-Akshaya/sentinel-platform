# Stage 4B — Secret Handling Note

## Do not commit these files

```text
.env
.env.local
.env.*.local
*.secret
*apikey*
```

## Safe Git check

Before every commit, run:

```powershell
git status
git diff --cached
```

If you see an API key, stop immediately.

## Local-only key storage

The API key is stored in:

```text
.env.local
```

This is acceptable for a local development demo, provided the file is ignored and never shared.

## Rotation rule

If a key is accidentally committed or pasted anywhere public, revoke it immediately and create a new one.
