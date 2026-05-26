# Sentinel v10.1 Stability and QA Notes

## Purpose

v10.1 is a bug-fix and stabilization release. It does not add new product features.

## Fixes

| Area | Fix |
|---|---|
| Launch Room data binding | Backend now returns both `final` and `freeze` aliases for compatibility |
| Launch Room fallback | Frontend now supports either `launchReadiness.final` or `launchReadiness.freeze` |
| CSS score card layout | Restored `.scoreRow` to three cards instead of an accidental 11-column layout |
| Tab layout | Keeps 11 tabs on large screens with responsive fallback |
| Final scope endpoint | Added `/api/product/final-scope` alias |
| Future stage wording | Removed version confusion from next-stage gates |
| Package cleanliness | This pack contains only v10.1 files, apply script, and README |

## Regression test checklist

1. Open `/api/health` and confirm `10.1.0`.
2. Open Final Room.
3. Export Final HTML.
4. Export Final JSON.
5. Open Launch Room.
6. Confirm Launch Readiness loads without page crash.
7. Confirm three score cards appear in one row on wide screen.
8. Run + Save Review to Vault.
9. Open Demo Room.
10. Open Delivery Kit.
11. Open Board Pack.
12. Open Evidence Requests.
13. Open Command Center.
14. Open Control Atlas.
15. Export Vault Backup.
16. Commit and tag v10.1.

## Stop condition

After v10.1, move to screenshots, demo recording, README polish, and GitHub presentation. Do not add another feature tab.
