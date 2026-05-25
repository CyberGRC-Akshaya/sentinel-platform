# Sentinel Assurance Platform

**AI-native assurance intelligence platform by Eye On Bits Pvt Ltd.**

Sentinel is an examiner-style assurance intelligence console for regulated organizations. It is designed to challenge evidence, metrics, vendor packages, privacy representations, SDLC artifacts, and AI governance claims.

Most GRC tools store evidence. Sentinel challenges whether the evidence is defensible.

---

## Current Release

**v0.4 — Report-Ready Examiner Console**

---

## What Sentinel does

Sentinel reviews structured evidence packages and produces:

- Assurance score
- Overall rating
- Severity distribution
- Top risk domains
- Examiner-style findings
- Evidence gaps
- Challenge questions
- Remediation guidance
- Framework relevance tags
- Downloadable JSON report
- Downloadable HTML examiner report

---

## Why this matters

In regulated environments, a control is not defensible merely because evidence exists.

Evidence must prove:

- source lineage
- reporting-period consistency
- denominator/numerator integrity
- reviewer approval
- management rationale
- vendor reliance logic
- privacy/data handling defensibility
- SDLC governance completion
- AI governance readiness

Sentinel is built around that practical assurance problem.

---

## Target users

- IT GRC teams
- CISOs / security governance leaders
- Internal Audit teams
- 2LOD / credible challenge teams
- TPRM teams
- Privacy teams
- AI governance teams
- SDLC / DevSecOps governance teams

---

## Current modules

### 1. IT Metrics Examiner

Challenges:
- denominator inconsistency
- cumulative vs periodic reporting mismatch
- screenshot-only evidence
- weak source-of-record linkage
- unsupported positive assurance statements

### 2. Vendor & Privacy Examiner

Challenges:
- incomplete SOC 2 reliance
- missing CUEC analysis
- missing data-flow evidence
- weak retention/data handling evidence
- customer data / NPI / PII defensibility gaps

### 3. SDLC & AI Governance Examiner

Challenges:
- missing security gates
- missing change approval evidence
- release governance gaps
- AI inventory/approval gaps
- missing monitoring and escalation evidence

---

## Screenshots to add

Add screenshots under:

```text
github-assets/
```

Recommended screenshots:

1. Sentinel homepage
2. Sample Case Library
3. Examiner Output
4. Severity Distribution
5. HTML Report Output

---

## Run locally

```powershell
docker compose up --build
```

Open:

```text
Frontend: http://localhost:3000
Backend health: http://localhost:8000/api/health
```

---

## API endpoints

```text
GET  /api/health
POST /api/analyze
POST /api/report-html
```

---

## Example use cases

- Pre-audit evidence readiness review
- IT metrics validation before committee reporting
- Vendor/SOC 2 reliance challenge
- Privacy evidence challenge
- AI governance readiness review
- SDLC release governance challenge

---

## Commercial service built around Sentinel

**Sentinel Evidence & Metrics Assurance Review**

A consulting-assisted review service where Sentinel accelerates:
- evidence analysis
- examiner-style questions
- finding generation
- remediation evidence requests
- executive reporting

See:

```text
sales/sentinel-assurance-review-service.md
```

---

## Disclaimer

Sentinel supports assurance review and professional judgment. It does not replace qualified audit, legal, regulatory, or compliance advice.

---

## Built by

**Eye On Bits Pvt Ltd**
