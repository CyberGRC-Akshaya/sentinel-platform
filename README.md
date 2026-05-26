# Sentinel Evidence Defensibility Workbench

**Company:** Eye On Bits Pvt Ltd  
**Version:** v10 Final Launch Edition  
**Status:** Local demo-grade product baseline

## Product positioning

Sentinel is an evidence defensibility challenge layer for audit, risk, compliance, TPRM, privacy, SDLC, IAM, and AI governance reviews.

It does not replace GRC repositories. It sits above evidence packages and challenges whether evidence is strong enough for audit, management review, 2LOD credible challenge, or examiner-style scrutiny.

## One-line value proposition

Sentinel turns weak evidence packages into findings, evidence requests, control mappings, board-ready narratives, and closure-ready remediation workflows.

## Product screenshots

Add screenshots under `github-assets/screenshots/` using the exact filenames below:

| Screenshot | Filename |
|---|---|
| Final Room | `01-final-room.png` |
| Launch Room | `02-launch-room.png` |
| Demo Room | `03-demo-room.png` |
| Control Atlas | `04-control-atlas.png` |
| Evidence Requests | `05-evidence-requests.png` |
| Board Pack | `06-board-pack.png` |
| Delivery Kit | `07-delivery-kit.png` |
| Portfolio Dashboard | `08-portfolio-dashboard.png` |
| Command Center | `09-command-center.png` |

## Core capabilities

| Capability | What it does |
|---|---|
| Evidence Intake | Accepts JSON, CSV, TXT, and MD evidence packages |
| Evidence Defensibility Scoring | Scores evidence quality across practical audit/review dimensions |
| Review Vault | Saves reviews locally for reload and export |
| Control Atlas | Maps evidence to control themes, expected artifacts, and missing control evidence |
| Evidence Request Studio | Converts findings into owner-ready evidence requests |
| Closure Readiness Engine | Scores whether remediation items are ready for closure |
| Board Pack Studio | Converts technical findings into executive-ready narrative |
| Executive Demo Room | Packages the product story, buyer value, and pilot offer |
| Delivery Kit | Creates checklist, follow-up note, and demo asset manifest |
| Portfolio Dashboard | Aggregates saved reviews, domains, severities, and open remediation items |
| Exports | HTML, JSON, and CSV outputs |

## Demo workflow

1. Open **Final Room** and explain product positioning.
2. Open **Launch Room** and show launch readiness.
3. Click **Run + Save Review to Vault**.
4. Open **Control Atlas** and show mapped control evidence gaps.
5. Open **Evidence Requests** and show owner-ready evidence asks.
6. Open **Board Pack** and show executive narrative.
7. Open **Command Center** and update remediation fields.
8. Open **Delivery Kit** and export handoff assets.
9. Export **Final HTML**, **Board HTML**, **Request CSV**, **Register CSV**, and **Vault Backup**.

## Run locally

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:3000
```

Backend health:

```text
http://localhost:8000/api/health
```

Expected backend after hotfix:

```json
"version": "10.1.1"
```

## Commercial pilot offer

### Evidence Defensibility Sprint

**Duration:** 2 weeks

**Outcome:** Find weak evidence before audit, examiners, management committees, or 2LOD credible challenge expose it.

**Deliverables:**

- evidence defensibility review
- findings register
- evidence request list
- Control Atlas mapping
- board-ready summary
- closure readiness tracker
- remediation action plan
- client delivery kit

## Important boundary

This is a local demo-grade product baseline. Production use requires authentication, authorization, hardened deployment, data protection controls, secure secrets management, monitoring, and formal legal/security review.
