# Sentinel Evidence Defensibility Workbench

**Company:** Eye On Bits Pvt Ltd  
**Version:** v10.2 GitHub Demo Packaging Edition  
**Status:** Local demo-grade product baseline

---

## What Sentinel is

Sentinel is an **evidence defensibility challenge layer** for audit, risk, compliance, TPRM, privacy, SDLC, IAM, and AI governance reviews.

It does not try to replace GRC repositories. It sits above evidence packages and asks the harder question:

> Is this evidence strong enough for audit, management review, 2LOD credible challenge, or examiner-style scrutiny?

---

## One-line value proposition

Sentinel turns weak evidence packages into **findings, evidence requests, control mappings, board-ready narratives, and closure-ready remediation workflows**.

---

## Why this matters

Many teams already have evidence. The problem is that the evidence is often:

- screenshot-only
- missing source lineage
- missing denominator or calculation logic
- missing reviewer approval
- weakly mapped to control objectives
- unclear on reporting period
- incomplete for SOC 2 / CUEC / privacy / AI / IAM / SDLC review
- not ready for audit or regulator-style challenge

Sentinel helps identify these gaps before they become audit findings, management surprises, or painful rework.

---

## Core capabilities

| Capability | What it does |
|---|---|
| Evidence Intake | Accepts JSON, CSV, TXT, and MD evidence packages |
| Evidence Defensibility Score | Scores source lineage, completeness, calculation integrity, approval, reporting-period alignment, governance traceability, and data handling |
| Review Vault | Saves reviews locally for reload and export |
| Control Atlas | Maps evidence to control themes and expected artifacts |
| Evidence Request Studio | Converts findings into owner-ready evidence requests |
| Closure Readiness Engine | Scores whether remediation items are ready for closure |
| Board Pack Studio | Converts technical findings into executive-ready narrative |
| Demo Room | Packages the product story, buyer value, and pilot offer |
| Delivery Kit | Creates checklist, follow-up note, and demo asset manifest |
| Launch / Final Room | Captures positioning, scope, offer, and next-stage gates |
| Portfolio Dashboard | Aggregates saved reviews, risk domains, severities, and open items |
| Exports | HTML, JSON, and CSV outputs |

---

## Tech stack

| Layer | Tool |
|---|---|
| Frontend | Next.js |
| Backend | FastAPI |
| Local Data Store | SQLite |
| Containerization | Docker Compose |
| Language | TypeScript, Python |
| Repo | GitHub |

---

## Run locally

Open Docker Desktop first. Then run:

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
docker compose down --remove-orphans
docker compose up --build
```

Open the app:

```text
http://localhost:3000
```

Check backend health:

```text
http://localhost:8000/api/health
```

Expected current version after hotfix:

```json
"version": "10.1.1"
```

---

## Recommended demo flow

1. Open **Final Room** and explain product positioning.
2. Open **Launch Room** and show launch readiness.
3. Run **Run + Save Review to Vault**.
4. Open **Control Atlas** and show mapped control gaps.
5. Open **Evidence Requests** and show owner-ready asks.
6. Open **Board Pack** and show executive narrative.
7. Open **Command Center** and update remediation fields.
8. Open **Delivery Kit** and export handoff assets.
9. Export **Final HTML**, **Board HTML**, **Request CSV**, **Register CSV**, and **Vault Backup**.

---

## Sample use cases

| Use Case | Example |
|---|---|
| IT Metrics Review | Validate source lineage, denominator consistency, calculation logic, and committee reporting evidence |
| TPRM / SOC 2 Review | Challenge SOC 2 reliance, CUEC analysis, bridge letter, subservice organizations, data flow, and residual risk |
| Privacy / Data Handling | Check customer data flow, retention, deletion, DPA, and access boundary evidence |
| SDLC / Change Governance | Review change record, security testing, deployment evidence, risk acceptance, and rollback evidence |
| AI Governance | Validate AI inventory, risk tier, approval, monitoring plan, and incident escalation evidence |
| IAM / Access Governance | Review access approval, MFA evidence, access reviews, exceptions, and revocation evidence |

---

## Commercial pilot offer

### Evidence Defensibility Sprint

**Duration:** 2 weeks

**Outcome:** Find weak evidence before audit, examiners, management committees, or 2LOD credible challenge expose it.

**Deliverables:**

- Evidence defensibility review
- Findings register
- Evidence request list
- Control Atlas mapping
- Board-ready summary
- Closure readiness tracker
- Remediation action plan
- Client delivery kit

---

## Important boundary

This is a local demo-grade product baseline. Production use requires authentication, authorization, hardened deployment, data protection controls, secure secrets management, monitoring, and formal legal/security review.

---

## Next-stage gates

| Stage | Gate |
|---|---|
| AI Reasoning Layer | Add real OpenAI-assisted reasoning with prompt logging and evidence-grounded outputs |
| Hosted Product Layer | Add PostgreSQL, authentication, users, tenant boundaries, and deployment hardening |
| Automation Layer | Add n8n / Google Workspace workflows for evidence owner follow-up and tracker updates |

---

## Repository status

This repository is currently positioned as a **portfolio-grade product prototype** and consulting-offer accelerator.

Next work should focus on:

- screenshots
- demo recording
- GitHub presentation
- UI bug fixes
- README polish
- sample evidence packs
- buyer conversations

No new feature tabs should be added until a deliberate next-stage architecture decision is made.
