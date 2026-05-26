# Sentinel v4.0 Portfolio Command Center

## What v4.0 adds

v4.0 upgrades Sentinel from a single-review workbench into a portfolio-level assurance command center.

## Major capabilities

| Capability | Description |
|---|---|
| Portfolio API | Aggregates all saved reviews from the local SQLite vault |
| Portfolio dashboard | Shows saved reviews, average scores, open remediation items, recurring domains, and severity mix |
| Portfolio HTML report | Exports an executive snapshot across saved reviews |
| Demo seed endpoint | Creates realistic sample reviews for demonstration |
| Portfolio JSON export | Exports portfolio-level analytics for reuse |

## New API endpoints

```text
GET /api/portfolio
GET /api/portfolio/report-html
POST /api/demo/seed
```

## Demonstration workflow

1. Start Docker.
2. Open Sentinel.
3. Click Portfolio tab.
4. Click Seed Demo Reviews.
5. Refresh Portfolio.
6. Export Portfolio HTML Report.
7. Load individual saved reviews from the Review Vault.
8. Update remediation register.
9. Save Register.
10. Refresh Portfolio again.

## Commercial positioning

This version is much stronger for portfolio, interview, and consulting demonstration because it shows how multiple reviews can roll up into an executive-level evidence assurance dashboard.
