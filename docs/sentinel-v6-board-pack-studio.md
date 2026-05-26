# Sentinel v6.0 Board Pack Studio

## What v6.0 adds

v6.0 upgrades Sentinel from a review and control-mapping tool into a management communication workbench.

## Major capabilities

| Capability | Description |
|---|---|
| Board Pack JSON | Generates structured board-pack data from saved review results |
| Board Pack HTML | Produces a board-ready standalone HTML report |
| Portfolio Board Pack | Produces portfolio-level board summary across saved reviews |
| Executive Narrative | Converts review scores into business-facing narrative |
| Board Message | Summarizes why evidence defensibility matters |
| Board Questions | Creates management-level questions for oversight |
| Management Response Prompts | Provides direct prompts for control owners |
| 30-Day Action Plan | Provides phased remediation plan |
| High-Priority Finding Summary | Extracts high/critical issues into board-ready format |

## New API endpoints

```text
GET /api/reviews/{review_id}/board-pack
GET /api/reviews/{review_id}/board-pack-html
GET /api/portfolio/board-pack-html
```

## Why this matters

A buyer does not only want findings. A buyer wants to know:
- what to say to leadership
- what to ask control owners
- what to remediate first
- what missing evidence blocks closure
- how to communicate the risk without drowning in technical detail

v6.0 creates that communication layer.
