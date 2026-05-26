# Sentinel Evidence Defensibility Workbench

**Company:** Eye On Bits Pvt Ltd  
**Version:** v10 Final Launch Edition  
**Status:** Local demo-grade product baseline

---

## Product positioning

Sentinel is an **evidence defensibility challenge layer** for audit, risk, compliance, TPRM, privacy, SDLC, IAM, and AI governance reviews.

It does not replace GRC repositories. It sits above evidence packages and challenges whether evidence is strong enough for audit, management review, 2LOD credible challenge, or examiner-style scrutiny.

---

## One-line value proposition

Sentinel turns weak evidence packages into **findings, evidence requests, control mappings, board-ready narratives, and closure-ready remediation workflows**.

---

## Why this exists

Most teams do not fail because they have no evidence.

They fail because evidence is often:

- screenshot-only
- missing source lineage
- missing denominator or calculation logic
- missing reviewer approval
- unclear on reporting period
- weakly mapped to control objectives
- incomplete for SOC 2 / CUEC / privacy / AI / IAM / SDLC review
- not closure-ready

Sentinel converts these weaknesses into structured findings, evidence asks, control mappings, remediation actions, and leadership-ready outputs.

---

## Core workflow

```text
Evidence Package
      ↓
Defensibility Review
      ↓
Findings + Scorecard
      ↓
Control Atlas Mapping
      ↓
Evidence Request Studio
      ↓
Closure Readiness
      ↓
Board Pack + Delivery Kit
```

---

## Capability stack

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

---

## Sample use cases

| Use Case | Sentinel Review Focus |
|---|---|
| IT Metrics Review | Source lineage, denominator consistency, calculation logic, committee reporting tie-out |
| TPRM / SOC 2 Review | SOC 2 reliance, CUEC mapping, bridge letter, subservice orgs, residual risk |
| Privacy / Data Handling | Data flow, retention, deletion, DPA, customer information boundaries |
| SDLC / Change Governance | Change record, release approval, testing evidence, rollback planning |
| AI Governance | AI inventory, risk tier, approval evidence, monitoring, incident escalation |
| IAM / Access Governance | Access approvals, MFA evidence, access review, exceptions, revocation |

---

## Tech stack

| Layer | Tool |
|---|---|
| Frontend | Next.js |
| Backend | FastAPI |
| Local Data Store | SQLite |
| Containerization | Docker Compose |
| Languages | TypeScript, Python |
| Repository | GitHub |

---

## Run locally

Open Docker Desktop first.

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

---

## Recommended walkthrough

1. Open **Final Room** and explain product positioning.
2. Open **Launch Room** and show readiness.
3. Click **Run + Save Review to Vault**.
4. Open **Control Atlas** and show mapped evidence gaps.
5. Open **Evidence Requests** and show owner-ready evidence asks.
6. Open **Board Pack** and show executive narrative.
7. Open **Command Center** and update remediation fields.
8. Open **Delivery Kit** and export handoff assets.

---

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

---

## Important boundary

This is a local demo-grade product baseline. Production use requires authentication, authorization, hardened deployment, data protection controls, secure secrets management, monitoring, and formal legal/security review.

---

## Next-stage gates

| Stage | Gate |
|---|---|
| AI Reasoning Layer | Real OpenAI-assisted reasoning with prompt logging and evidence-grounded outputs |
| Hosted Product Layer | PostgreSQL, authentication, user accounts, tenant boundaries, deployment hardening |
| Automation Layer | n8n / Google Workspace workflows for evidence owner follow-up and tracker updates |
