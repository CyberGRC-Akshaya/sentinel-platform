# Sentinel v2.1 Evidence Intake Intelligence Methodology

## What v2.1 adds

Sentinel v2.1 adds evidence intake intelligence on top of the v2.0 defensibility scoring engine.

## New diagnostics

| Diagnostic | Meaning |
|---|---|
| Metadata Completeness Score | Checks whether evidence item has owner, source system, reporting period, evidence date, and control reference |
| Intake Coverage Score | Checks whether expected evidence elements for the detected domain are present |
| Artifact Profile | Infers artifact type such as metric evidence, SOC 2 evidence, IAM evidence, AI governance evidence, or release evidence |
| Missing Metadata | Lists metadata fields that should be collected |
| Missing Intake Elements | Lists missing evidence elements expected for the review domain |

## Why this matters

Before an auditor or 2LOD reviewer challenges the quality of evidence, the first problem is often intake quality.

Many evidence packages fail because:
- no owner is captured
- source system is unclear
- reporting period is not tied out
- evidence date is missing
- control reference is absent
- expected domain-specific evidence is missing

v2.1 makes these gaps visible upfront.

## Correct use

Use v2.1 to perform an intake readiness review before deeper assurance analysis.
