# Stage 2 Branch and Commit Guide

## Step 1 — Open PowerShell in project folder

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
```

## Step 2 — Check current state

```powershell
git status
```

## Step 3 — Create branch

```powershell
git checkout -b stage-2-code-stabilization
```

If branch already exists:

```powershell
git checkout stage-2-code-stabilization
```

## Step 4 — Commit this Stage 2 VS Code pack

```powershell
git add docs scripts manual-refactor-prompts
git commit -m "Add Stage 2 VS Code stabilization workflow"
git push -u origin stage-2-code-stabilization
```

## Rule

Commit only working code.

Never commit broken build unless it is a separate branch specifically for debugging.
