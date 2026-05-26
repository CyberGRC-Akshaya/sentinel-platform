# Sentinel v3.0 Review Vault Architecture

## What v3.0 changes

This is not a cosmetic upgrade.

Sentinel v3.0 adds a persistent local review vault using SQLite.

## New platform capabilities

| Capability | Description |
|---|---|
| Persistent Review Vault | Saves reviews to `backend/data/sentinel.db` |
| Saved remediation register | Stores owner, target date, status, management response, closure evidence, and validation notes |
| Reload after restart | Reviews can be loaded again after Docker restart if `backend/data` remains present |
| Save Register button | Saves edited remediation tracker back to backend |
| Delete review | Deletes saved review from vault |
| Saved report endpoint | Generates HTML report from saved review |
| Docker volume mapping | Persists SQLite file through local bind mount |

## New API endpoints

```text
POST /api/reviews/analyze-save
GET /api/reviews
GET /api/reviews/{review_id}
PUT /api/reviews/{review_id}/register
DELETE /api/reviews/{review_id}
GET /api/reviews/{review_id}/report-html
```

## Why this matters

Earlier versions generated findings, but the workflow was still disposable.

v3.0 turns Sentinel into a practical local workbench where a reviewer can:
1. Run review
2. Save review
3. Edit remediation register
4. Save register
5. Close laptop / restart Docker
6. Reload saved review
7. Export updated register and report

## Important limitation

This is still a local prototype. It is not enterprise SaaS. It does not yet include:
- authentication
- RBAC
- encrypted database
- multi-user workflow
- audit logs
- tenant isolation
- production deployment hardening
