# Stage 2 Code Inventory Hotfix Note

## Issue

The previous inventory script failed with:

```text
The string is missing the terminator: "
```

## Cause

The script contained fragile quoting around report-path/report-writing logic.

## Fix

This hotfix replaces only:

```text
scripts/stage-2/stage-2-code-inventory.ps1
```

It does not modify application code.

## Run

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-code-inventory.ps1
```

## Output

```text
docs\stage-2-code-stabilization\STAGE_2_CODE_INVENTORY_REPORT.txt
```
