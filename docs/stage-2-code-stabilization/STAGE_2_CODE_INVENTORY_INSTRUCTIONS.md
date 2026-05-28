# Stage 2 Code Inventory Instructions

## Purpose

Before refactoring, we need a clean inventory of:

- frontend file size
- backend file size
- tabs
- API calls
- backend routes
- backend functions
- CSS risk indicators
- Docker config status

This is inspection only. It does not modify app code.

## Run

Open PowerShell in:

```text
C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-code-inventory.ps1
```

## Output

The script creates:

```text
docs\stage-2-code-stabilization\STAGE_2_CODE_INVENTORY_REPORT.txt
```

## Next

Open the report and share the output.

Then we decide the first safe stabilization task.
