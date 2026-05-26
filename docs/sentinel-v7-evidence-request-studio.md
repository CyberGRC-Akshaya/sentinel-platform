# Sentinel v7.0 Evidence Request Studio

## What v7.0 adds

v7.0 upgrades Sentinel from a findings and board-pack workbench into an evidence follow-up workflow engine.

## Major capabilities

| Capability | Description |
|---|---|
| Evidence Request Studio | Converts findings into request-ready evidence asks |
| Request Message Generator | Creates owner-ready request text |
| Preferred Artifact List | Converts missing evidence into artifact requests |
| Closure Criteria | Defines what must be true before closure |
| Validation Test | Gives reviewer test criteria for each evidence request |
| Closure Readiness Engine | Scores whether remediation register rows are ready for closure |
| Evidence Request HTML | Creates standalone evidence request pack |
| Evidence Request CSV | Exports request list for tracker, email, Sheets, or n8n workflow |

## New API endpoints

```text
GET /api/reviews/{review_id}/request-studio
GET /api/reviews/{review_id}/request-studio-html
```

## Why this matters

Most GRC tools stop at findings. Real work begins after findings:
- who owns the gap
- what evidence is needed
- what artifact would close it
- what validation test confirms closure
- what remains missing before closure

v7.0 starts operationalizing that follow-up workflow.
