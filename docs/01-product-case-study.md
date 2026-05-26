# Sentinel Product Case Study

## Context

Governance, risk, compliance, audit, privacy, TPRM, IAM, SDLC, and AI governance teams often collect evidence for controls, metrics, vendors, access reviews, releases, and risk decisions.

But evidence collection alone does not prove defensibility.

The harder question is:

> Can the evidence survive audit, management review, 2LOD credible challenge, or examiner-style scrutiny?

## Problem

Evidence packages often contain practical weaknesses:

- screenshots without source exports
- metric values without denominator support
- control claims without mapped evidence
- SOC 2 reports without CUEC analysis
- vendor reviews without data-flow evidence
- AI use cases without inventory/risk-tier support
- IAM reviews without exception or revocation evidence
- remediation items without closure criteria

## Solution

Sentinel reviews evidence packages and produces:

- defensibility score
- findings register
- evidence request list
- control atlas mapping
- closure readiness tracker
- board-ready narrative
- delivery checklist

## Product architecture

```text
Frontend: Next.js
Backend: FastAPI
Database: SQLite
Runtime: Docker Compose
Exports: HTML, JSON, CSV
```

## Differentiation

Sentinel does not act as a passive evidence repository.

It acts as a challenge layer.

It asks:

- What is the control claim?
- What evidence supports it?
- What evidence is missing?
- What would an auditor or examiner ask next?
- What evidence request should go to the owner?
- Is the item ready for closure?

## Commercial pathway

Sentinel can support a productized service:

**Evidence Defensibility Sprint**

A two-week evidence challenge review for teams preparing for audit, management committee reporting, vendor review, AI governance review, IAM review, or SDLC governance review.
