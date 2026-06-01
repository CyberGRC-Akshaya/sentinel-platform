# Stage 4 — AI Governance Boundary

## Positioning

Sentinel's AI layer is an assistant, not an autonomous decision-maker.

## Human review requirement

AI-generated content must be reviewed before use in:

- audit workpapers
- management reports
- evidence requests
- board summaries
- client deliverables
- regulatory responses

## Data handling rule

During Stage 4 testing, use only:

- sample evidence
- synthetic evidence
- sanitized evidence
- non-client confidential test data

Do not paste real customer data, NPI, PII, or client confidential information into AI prompts.

## Logging expectation

For every AI assist request, preserve:

- timestamp
- review ID if available
- AI capability used
- model name
- input summary
- response summary
- failure status if applicable

Do not log full secrets or API keys.

## Claim boundary

Approved language:

```text
AI-assisted evidence narrative and drafting support.
```

Avoid:

```text
Automated audit conclusion.
Regulatory-approved AI.
Autonomous examiner.
Production AI governance engine.
```
