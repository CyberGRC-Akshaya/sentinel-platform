# Stage 4 — Current Next Actions

## Current action

Run Stage 4 AI inventory before modifying backend code.

## Commands

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
git switch -c stage-4-real-ai-integration
powershell -ExecutionPolicy Bypass -File .\scripts\stage-4\stage-4-ai-inventory.ps1
```

If branch already exists:

```powershell
git switch stage-4-real-ai-integration
```

## Share output

Share:

```text
docs\stage-4-ai-integration\STAGE_4_AI_INVENTORY_REPORT.txt
```

## Do not

- add OpenAI code yet
- paste API keys into chat
- change frontend yet
- change Docker yet
