# Sentinel Evidence Defensibility Workbench

**Version:** v10.0 Final Launch Edition  
**Company:** Eye On Bits Pvt Ltd  
**Status:** Local demo-grade product baseline

## Positioning

Sentinel is an evidence defensibility challenge layer for audit, risk, compliance, TPRM, privacy, SDLC, IAM, and AI governance reviews.

It is not a GRC repository. It sits above evidence packages and challenges whether the evidence is strong enough for audit, management review, 2LOD credible challenge, or examiner-style scrutiny.

## One-liner

Sentinel turns weak evidence packages into findings, evidence requests, control mappings, board-ready narratives, and closure-ready remediation workflows.

## Capability stack

- Evidence intake
- Evidence defensibility scoring
- Persistent local review vault
- Control Atlas mapping
- Evidence Request Studio
- Closure Readiness Engine
- Board Pack Studio
- Executive Demo Room
- Delivery Kit
- Launch Room
- Final Room
- Portfolio dashboard
- HTML, JSON, and CSV exports
- Docker-based local execution

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

## Recommended demo flow

1. Open Final Room.
2. Open Launch Room.
3. Run + Save Review to Vault.
4. Open Demo Room.
5. Open Control Atlas.
6. Open Evidence Requests.
7. Open Board Pack.
8. Open Delivery Kit.
9. Export Final HTML, Launch HTML, Board HTML, Request CSV, Register CSV, and Vault Backup.

## Commercial offer

**Evidence Defensibility Sprint**  
Duration: 2 weeks

Outcome: Find weak evidence before audit, examiners, management committees, or 2LOD credible challenge expose it.

## Important boundary

This edition is a local demo-grade product baseline. Production use requires authentication, authorization, hardened deployment, data protection controls, secure secrets management, monitoring, and formal legal/security review.
