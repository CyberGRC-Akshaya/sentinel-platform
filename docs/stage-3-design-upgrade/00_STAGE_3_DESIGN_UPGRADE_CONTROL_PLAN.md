# Stage 3 — Design Upgrade Control Plan

## Objective

Make Sentinel look premium, enterprise-grade, and demo-ready without breaking the working Stage 2 baseline.

## Stage 3 rule

Design polish only. No new features.

## Allowed

- spacing cleanup
- typography hierarchy
- card and panel consistency
- tab readability
- button hierarchy
- dashboard polish
- report/workflow readability
- empty state improvement
- screenshot readiness

## Not allowed

- backend changes
- scoring logic changes
- new tabs
- new workflows
- OpenAI integration
- PostgreSQL
- n8n
- deployment
- full rewrite of page.tsx

## Design direction

Sentinel should feel like:

- senior management / boardroom ready
- audit and GRC professional
- dark premium control-room style
- clear evidence workflow
- not a student project
- not a toy dashboard

## Stage 3 exit gates

| Gate | Required Result |
|---|---|
| UI opens cleanly | `localhost:3000` loads |
| No build error | Docker build passes |
| Core workflow intact | Run + Save Review works |
| Vault intact | Saved review loads |
| Export intact | JSON/CSV/HTML downloads work |
| Screenshots ready | 3–5 core screenshots can be captured |
| Git clean | changes committed and pushed |
