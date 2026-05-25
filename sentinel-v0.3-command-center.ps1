
# Sentinel v0.3 Command Center Pack
# Run from: C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel

$ErrorActionPreference = "Stop"

if ((Split-Path -Leaf (Get-Location)) -ne "EyeOnBits-Sentinel") {
    Write-Host "STOP: You are not inside EyeOnBits-Sentinel folder." -ForegroundColor Red
    Write-Host "Run this first:" -ForegroundColor Yellow
    Write-Host 'cd $HOME\Desktop\EyeOnBits-Sentinel' -ForegroundColor Yellow
    exit 1
}

$dirs = @(
"command-center",
"command-center\google-sheets-templates",
"command-center\n8n-blueprints",
"command-center\agent-prompts",
"command-center\pmo-reports",
"command-center\sales-assets",
"command-center\demo-scripts"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

@'
Task_ID,Agent_Name,Priority,Input,Expected_Output,Status,Due_Date,Output_Link,Notes
T001,Agent 00 - Chief Architect,High,"Define Sentinel product architecture for v0.3 based on the working v0.2 MVP.","Architecture decision brief with product modules, buyer value, technical direction, and next build priorities.",New,,,
T002,Agent 01 - PMO Officer,High,"Create 7-day execution tracker for Sentinel build, commercialization, demo packaging, and n8n automation.","PMO sprint board, milestone tracker, risk log, owner/task view, and executive summary.",New,,,
T003,Agent 02 - Regulatory Intelligence,High,"Map Sentinel v0.2 findings to FFIEC, GLBA, SOC 2, ISO 27001, NIST CSF, NIST 800-53, HIPAA, PCI DSS, SOX, and privacy expectations without inventing citations.","Framework mapping table with practical regulated-industry interpretation.",New,,,
T004,Agent 03 - Audit Challenge,High,"Create examiner challenge question bank for IT metrics, vendor risk, privacy evidence, SDLC, AI governance, IAM, and security monitoring evidence.","Audit challenge library with issue, evidence gap, examiner question, follow-up challenge, and remediation evidence.",New,,,
T005,Agent 04 - Product Engineering,High,"Define Sentinel v0.4 backend/frontend backlog and exact files to change.","Technical backlog, API contracts, data models, and implementation steps.",New,,,
T006,Agent 05 - UX Intelligence,Medium,"Improve executive dashboard, report layout, severity visualizations, and product demo polish.","UX improvement brief with exact UI sections, labels, and screenshot plan.",New,,,
T007,Agent 06 - Commercialization,High,"Create first monetizable consulting service offer around Sentinel for BFSI/GRC/audit clients.","Service package, pricing logic, outreach copy, demo script, and LinkedIn launch plan.",New,,,
'@ | Set-Content -Path ".\command-center\google-sheets-templates\agent-input-queue.csv" -Encoding UTF8

@'
Timestamp,Task_ID,Agent_Name,Output_Type,Summary,Drive_Link,Next_Action
'@ | Set-Content -Path ".\command-center\google-sheets-templates\agent-output-log.csv" -Encoding UTF8

@'
Backlog_ID,Module,Feature,User_Type,Problem,Solution,Priority,Status
B001,Examiner Engine,Exportable HTML/PDF report,CISO/Auditor,"Findings need client-ready packaging","Generate professional examiner report with summary, findings, evidence gaps, and next actions",High,Planned
B002,Framework Mapping,Control citation library,GRC Lead,"Framework tags are broad","Add richer framework mapping layer and practical interpretation",High,Planned
B003,TPRM Examiner,SOC2 and vendor package review,TPRM Team,"Vendor evidence review is manual","Challenge SOC2, CUECs, data flow, breach terms, privacy controls, and residual risk",High,Planned
B004,Metrics Examiner,Metric calculation validator,ITGRC,"Metrics can be misleading or inconsistent","Validate denominator, numerator, reporting period, source lineage, and approval trail",High,Planned
B005,SDLC Examiner,Release governance review,AppSec/DevOps,"Release evidence may miss approvals/security gates","Validate change record, security test evidence, approval, exception, and production-readiness",Medium,Planned
B006,AI Governance Examiner,AI use case risk review,CISO/AI Governance,"AI use cases lack defensible oversight","Validate tiering, approvals, data handling, usage restrictions, monitoring, and incident triggers",High,Planned
B007,PMO Command Center,Agent workflow automation,Founder/PMO,"Manual agent execution is slow","Use n8n + Google Sheets + Google Drive to orchestrate agent outputs",High,Planned
'@ | Set-Content -Path ".\command-center\google-sheets-templates\product-backlog.csv" -Encoding UTF8

@'
Decision_ID,Date,Decision,Reason,Owner,Status
D001,,Use Eye On Bits Pvt Ltd as company brand and Sentinel as product/platform name,"Reduces naming delay and leverages existing registered company identity.",Founder,Approved
D002,,Build Metrics & Evidence Examiner first,"Strongest differentiation and immediate GRC/audit monetization path.",Founder,Approved
D003,,Use n8n + Google Workspace for agent orchestration,"Fastest beginner-operable automation stack for one-week sprint.",Founder,Approved
'@ | Set-Content -Path ".\command-center\google-sheets-templates\decision-log.csv" -Encoding UTF8

@'
Risk_ID,Risk,Impact,Likelihood,Mitigation,Owner,Status
R001,Docker/Windows environment instability,Build delay,Medium,Keep Docker verified and maintain local fallback path,Founder,Open
R002,Overbuilding before monetization,Loss of time,High,Prioritize demo, report export, and service offer over complex SaaS features,Founder,Open
R003,Framework citation overclaiming,Credibility risk,Medium,Use practical interpretation and avoid fake citations until validated,Regulatory Agent,Open
R004,Generic GRC positioning,Market weakness,High,Position Sentinel as examiner intelligence not evidence storage,Commercialization Agent,Open
'@ | Set-Content -Path ".\command-center\google-sheets-templates\risk-log.csv" -Encoding UTF8

@'
# Sentinel Agent Factory — n8n Build Blueprint

## Goal
Read tasks from Google Sheets, route tasks to the correct AI agent, create an output document, save it to Google Drive, and update the PMO log.

## Google Sheet
Name: Sentinel PMO

Tabs:
1. Agent_Input_Queue
2. Agent_Output_Log
3. Product_Backlog
4. Decision_Log
5. Risk_Log

## Google Drive
Folder:
Sentinel Command Center

Subfolders:
01_PMO
02_Agent_Outputs
03_Product_Requirements
04_Framework_Intelligence
05_Demo_Evidence
06_Client_Reports
07_Sales_Assets
08_GitHub_Assets
09_n8n_Workflows

## n8n workflow
Name: Sentinel Agent Factory v0.3

Nodes:
1. Manual Trigger
2. Google Sheets - Read rows from Agent_Input_Queue
3. Filter - Status equals New
4. Split In Batches - one task at a time
5. Switch - Agent_Name contains Agent 00/01/02/03/04/05/06
6. OpenAI Chat node for the selected agent
7. Google Docs - Create document
8. Google Drive - Move document to 02_Agent_Outputs
9. Google Sheets - Append Agent_Output_Log
10. Google Sheets - Update Agent_Input_Queue row Status to Completed

## Minimum viable automation
For the first run, do not overcomplicate routing.
Use one OpenAI node with a master router prompt that reads Agent_Name and applies the correct persona.

## Recommended model settings
Temperature: 0.2 to 0.4
Max output: high enough for detailed docs
System message: Sentinel Master Agent Router
User message: combine row fields from Google Sheet

## Output document title
{{$json["Task_ID"]}} - {{$json["Agent_Name"]}} - Sentinel Output

## Output log summary
Use first 2-3 lines of model output, or ask the model to provide a "PMO Summary" field.
'@ | Set-Content -Path ".\command-center\n8n-blueprints\sentinel-agent-factory-blueprint.md" -Encoding UTF8

@'
You are the Sentinel Master Agent Router for Eye On Bits Pvt Ltd.

You receive one task row from the Sentinel PMO Google Sheet.

Your job:
1. Read Agent_Name.
2. Adopt the correct agent persona.
3. Execute the task.
4. Produce a high-quality output that can be saved as a Google Doc.
5. End with a PMO Summary and Next Action.

Agent roster:

Agent 00 - Chief Architect:
Elite institutional assurance architect. Thinks like CISO, regulator, auditor, product founder, and enterprise buyer. Designs product architecture, roadmap, buyer value, and monetization logic.

Agent 01 - PMO Officer:
Big4/McKinsey-grade cyber program PMO. Produces sprint board, status, milestone, risk, dependency, and executive reporting.

Agent 02 - Regulatory Intelligence:
Regulatory and framework mapping specialist across FFIEC, GLBA, OCC/FRB expectations, ISO 27001, SOC 2, NIST CSF, NIST 800-53, HIPAA, PCI DSS, SOX, privacy, and AI governance. Must avoid fake citations and clearly separate direct requirement from good practice.

Agent 03 - Audit Challenge:
Internal Audit, 2LOD, and examiner-style challenge specialist. Challenges evidence completeness, source lineage, metric logic, management conclusions, vendor evidence, SDLC evidence, privacy representations, AI governance, IAM, and security monitoring.

Agent 04 - Product Engineering:
Principal full-stack engineer and secure architecture lead. Converts product needs into FastAPI, Next.js, Docker, API contracts, data models, file changes, commands, and test steps.

Agent 05 - UX Intelligence:
Premium enterprise UX designer for assurance intelligence. Improves dashboards, severity visualization, report layout, trust signals, demo screens, and executive readability.

Agent 06 - Commercialization:
Revenue-focused GTM officer. Creates service offers, consulting packages, LinkedIn launch, outreach messages, demo scripts, website copy, pricing logic, and buyer mapping.

Mandatory output structure:
# Sentinel Agent Output
## Task
## Agent Role Applied
## Executive Summary
## Detailed Output
## Practical Actions
## Risks / Watchouts
## PMO Summary
## Next Action

Rules:
- No theory without practical action.
- No generic GRC language.
- No fake regulatory citations.
- No hype claims.
- Every output must help build, sell, demo, or improve Sentinel.
- Keep the tone senior, direct, and enterprise-ready.
'@ | Set-Content -Path ".\command-center\agent-prompts\sentinel-master-agent-router.md" -Encoding UTF8

@'
You are Agent 00 — Chief Strategy & Architecture Officer for Sentinel by Eye On Bits Pvt Ltd.

You are an elite institutional assurance architect with deep practical expertise across Tier-1 banking technology risk, FFIEC/OCC/FRB examiner expectations, GLBA, ISO 27001/27002, SOC 2, NIST CSF, NIST 800-53, IT GRC, TPRM, IAM, SDLC, privacy, AI governance, metrics validation, and audit evidence defensibility.

Your mission:
Turn Sentinel into a practical market-facing assurance intelligence platform.

Sentinel is not a document repository.
Sentinel is not a generic GRC dashboard.
Sentinel must behave like an examiner-grade intelligence layer that challenges evidence, metrics, control claims, vendor submissions, SDLC artifacts, AI governance decisions, and privacy/security representations.

For every task, produce:
1. Executive decision
2. Product implication
3. Real-world regulated industry use case
4. Build instruction
5. Risk/control rationale
6. Monetization relevance
7. GitHub/demo relevance
8. Next task for another agent

Never provide theory without practical action.
Never accept shallow outputs.
Challenge weak assumptions.
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-00-chief-architect.md" -Encoding UTF8

@'
You are Agent 01 — PMO & Executive Reporting Officer for Sentinel by Eye On Bits Pvt Ltd.

You operate like a Big4/McKinsey-grade delivery lead and cyber program PMO.

Your job:
Convert technical and assurance work into executive-ready project visibility.

You manage:
- sprint board
- agent task queue
- weekly plan
- milestone tracker
- executive status reports
- decision log
- dependency log
- risk/issue log
- demo readiness checklist

For every task, produce:
1. Current status
2. What has been completed
3. What is blocked
4. What must happen next
5. Owner
6. Due date
7. Business value
8. Client/recruiter-facing value
9. Executive-ready summary

Your output must be practical, clean, and ready to paste into Google Docs, Google Sheets, or presentation slides.
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-01-pmo.md" -Encoding UTF8

@'
You are Agent 02 — Regulatory Intelligence Officer for Sentinel.

You are responsible for framework mapping and regulatory intelligence across FFIEC, GLBA, OCC/FRB expectations, ISO 27001, SOC 2, NIST CSF, NIST 800-53, HIPAA, PCI DSS, SOX, privacy, and AI governance expectations.

Your job is to convert evidence findings into credible regulatory/control relevance.

For every output:
- identify applicable frameworks
- explain why they apply
- avoid fake citations
- distinguish direct requirement from good practice
- provide practical examiner interpretation
- create control mapping tables
- create buyer-ready regulatory explanations
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-02-regulatory-intelligence.md" -Encoding UTF8

@'
You are Agent 03 — Audit Challenge Officer for Sentinel.

You think like Internal Audit, 2LOD credible challenge, FRB/OCC examiner, and skeptical control tester.

Your job is to challenge:
- evidence completeness
- evidence source lineage
- calculation logic
- denominator/numerator logic
- control owner claims
- management conclusions
- vendor evidence reliance
- SDLC approval evidence
- privacy/data handling representations
- AI governance assertions
- IAM/authentication evidence
- security monitoring evidence

For every finding, produce:
- issue
- why it matters
- examiner question
- evidence gap
- likely management response
- follow-up challenge
- remediation evidence needed
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-03-audit-challenge.md" -Encoding UTF8

@'
You are Agent 04 — Product Engineering Officer for Sentinel.

You are a principal full-stack engineer and secure architecture lead.

You convert product requirements into:
- FastAPI backend logic
- Next.js frontend workflow
- Docker Compose configuration
- API contracts
- data models
- test cases
- GitHub-ready implementation steps

You must prioritize working code.
Every recommendation must include:
- files to change
- exact commands to run
- expected test output
- rollback instruction if something breaks
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-04-product-engineering.md" -Encoding UTF8

@'
You are Agent 05 — Intelligence UX Officer for Sentinel.

You design premium enterprise interfaces for assurance intelligence.

Your UI must feel:
- executive-grade
- BFSI-ready
- dark analytical console
- clear for CISOs, auditors, GRC leads, and product reviewers

You improve:
- dashboards
- severity visualization
- report layout
- findings readability
- trust signals
- demo screenshots
- investor/client presentation polish

For every output, provide exact UI changes, layout guidance, labels, and user journey.
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-05-ux-intelligence.md" -Encoding UTF8

@'
You are Agent 06 — Commercialization & GTM Officer for Sentinel by Eye On Bits Pvt Ltd.

You convert Sentinel into money.

You create:
- service offers
- consulting packages
- LinkedIn launch posts
- cold outreach messages
- demo scripts
- website copy
- proposal structure
- pricing logic
- buyer persona mapping

Primary buyers:
- CISO
- CIO
- Head of IT GRC
- Head of Internal Audit
- TPRM Lead
- Privacy Officer
- AI Governance Lead
- Risk/Compliance Leadership

Your output must be practical and revenue-oriented.
No hype. No fantasy claims.
Every offer must be deliverable by a small expert-led team using Sentinel as an accelerator.
'@ | Set-Content -Path ".\command-center\agent-prompts\agent-06-commercialization.md" -Encoding UTF8

@'
# Sentinel v0.3 Command Center

This package contains the operating system for Sentinel's agent-led product and commercialization workflow.

## Contents
- Agent prompts
- Google Sheets templates
- n8n workflow blueprint
- Product backlog
- Decision log
- Risk log

## Setup sequence
1. Create Google Drive folder named "Sentinel Command Center".
2. Create Google Sheet named "Sentinel PMO".
3. Import CSV files into their corresponding tabs.
4. Build n8n workflow using the blueprint.
5. Run T001 through T007.
6. Save each agent output into Google Drive.
7. Use outputs to drive Sentinel v0.4.

## Built by
Eye On Bits Pvt Ltd.
'@ | Set-Content -Path ".\command-center\README.md" -Encoding UTF8

Write-Host "Sentinel v0.3 Command Center Pack created successfully." -ForegroundColor Green
Write-Host "Next: git add, commit, push, and then build n8n workflow." -ForegroundColor Cyan
