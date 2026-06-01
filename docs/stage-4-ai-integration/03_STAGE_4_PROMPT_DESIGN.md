# Stage 4 — Prompt Design

## Prompt principles

Prompts must be:

- narrow
- structured
- evidence-bound
- non-autonomous
- explicit about human review
- clear that scores come from Sentinel rule engine

## System prompt concept

```text
You are an evidence defensibility review assistant. 
You do not make final audit conclusions. 
You help improve clarity, evidence request wording, and executive review narratives based only on the supplied Sentinel review output.
```

## User prompt input shape

The prompt should include:

- organization
- industry
- review objective
- evidence type
- overall score
- rating
- findings summary
- missing evidence
- control mapping
- requested output type

## Output format

AI should return JSON or markdown sections:

```text
Executive Summary
Key Evidence Gaps
Evidence Requests
Reviewer Challenge Questions
Management-Ready Next Steps
Human Review Note
```

## Forbidden prompt behavior

Do not ask AI to:

- invent evidence
- cite unsupported regulatory references
- mark issues closed
- change risk rating
- decide acceptability
- process secrets or confidential data
