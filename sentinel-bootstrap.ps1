# Sentinel MVP Bootstrap Script
# Author: Eye On Bits / Sentinel setup
# Purpose: Creates a working FastAPI + Next.js + Docker MVP structure.
# Run from: C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel

$ErrorActionPreference = "Stop"

if ((Split-Path -Leaf (Get-Location)) -ne "EyeOnBits-Sentinel") {
    Write-Host "STOP: You are not inside EyeOnBits-Sentinel folder." -ForegroundColor Red
    Write-Host "Run this first:" -ForegroundColor Yellow
    Write-Host 'cd $HOME\Desktop\EyeOnBits-Sentinel' -ForegroundColor Yellow
    exit 1
}

$dirs = @(
"backend",
"backend/app",
"frontend",
"frontend/app",
"docs",
"sample-data",
"prompts",
"agents",
"architecture",
"reports",
"sales",
"workflows",
"screenshots",
"decks",
"docker",
"scripts",
"github-assets"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

@'
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.4
python-multipart==0.0.20
'@ | Out-File -FilePath "backend/requirements.txt" -Encoding utf8

@'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

app = FastAPI(
    title="Sentinel Assurance Engine",
    description="AI-native assurance intelligence engine by Eye On Bits for evidence validation, metric challenge, and examiner-style governance review.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvidenceItem(BaseModel):
    title: str
    content: str
    source_system: Optional[str] = None
    owner: Optional[str] = None
    reporting_period: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class AnalyzeRequest(BaseModel):
    organization: str
    industry: str
    evidence_type: str
    review_objective: str
    items: List[EvidenceItem]

def severity_weight(severity: str) -> int:
    return {"Critical": 25, "High": 18, "Medium": 10, "Low": 5}.get(severity, 5)

def finding(title, severity, issue, evidence_gap, examiner_question, remediation, frameworks, affected_item):
    return {
        "title": title,
        "severity": severity,
        "affected_item": affected_item,
        "issue": issue,
        "evidence_gap": evidence_gap,
        "examiner_question": examiner_question,
        "remediation": remediation,
        "framework_relevance": frameworks
    }

def analyze_item(item: EvidenceItem, evidence_type: str):
    text = f"{item.title} {item.content} {item.source_system or ''}".lower()
    findings = []

    if "denominator" in text and ("mismatch" in text or "different" in text or "changed" in text):
        findings.append(finding(
            "Metric Denominator Inconsistency",
            "High",
            "The metric narrative indicates that the denominator changed or differs across source evidence and reporting output.",
            "The evidence package does not clearly prove population completeness, denominator approval, or reconciliation to source-of-record.",
            "How did management validate that the denominator used in the reported metric is complete, accurate, and consistently applied for the reporting period?",
            "Add source-of-record extract, population logic, reconciliation notes, reviewer approval, and reporting-period tie-out.",
            ["FFIEC Management", "FFIEC Audit", "GLBA 501(b)", "NIST CSF Govern", "CRI Profile Governance"],
            item.title
        ))

    if "cumulative" in text and ("quarter" in text or "quarterly" in text):
        findings.append(finding(
            "Cumulative vs Periodic Reporting Logic Risk",
            "High",
            "The evidence suggests a possible mismatch between cumulative measurement and quarterly reporting interpretation.",
            "The metric definition does not clearly state whether the value is cumulative, point-in-time, rolling-period, or quarter-specific.",
            "Is the metric intended to represent quarterly activity or cumulative year-to-date performance, and how is that interpretation controlled?",
            "Clarify metric definition, align calculation logic to reporting intent, and retain reviewer sign-off for the interpretation.",
            ["FFIEC Management", "FFIEC Audit", "SOX-style reporting discipline", "CRI Profile Risk Measurement"],
            item.title
        ))

    if "screenshot" in text and ("only" in text or "manual" in text):
        findings.append(finding(
            "Weak Evidence Lineage",
            "Medium",
            "The evidence appears to rely heavily on screenshots or manual artifacts without system-of-record lineage.",
            "Screenshots alone may not demonstrate completeness, extraction parameters, source ownership, or calculation integrity.",
            "What source system produced this evidence, who extracted it, and how was completeness validated?",
            "Capture system export, timestamp, extractor identity, query/filter criteria, and independent review evidence.",
            ["FFIEC Audit", "NIST CSF Govern", "ISO 27001 Evidence and Monitoring Expectations"],
            item.title
        ))

    if "vendor" in text and ("soc 2" in text or "soc2" in text) and ("cuec" not in text):
        findings.append(finding(
            "Incomplete SOC 2 Reliance Analysis",
            "Medium",
            "SOC 2 evidence is referenced but complementary user entity controls are not clearly evaluated.",
            "The review may not prove whether customer-side responsibilities were identified, assigned, and operating.",
            "Which complementary user entity controls apply to the bank, and where is operating evidence retained?",
            "Document CUEC applicability, internal control ownership, evidence location, and residual risk conclusion.",
            ["AICPA SOC 2", "FFIEC Outsourcing Technology Services", "GLBA Vendor Oversight"],
            item.title
        ))

    if "pii" in text or "npi" in text or "customer data" in text:
        if "data flow" not in text and "dpa" not in text and "retention" not in text:
            findings.append(finding(
                "Privacy and Data Handling Evidence Gap",
                "High",
                "The artifact references sensitive customer or personal data but lacks clear data-flow, retention, or contractual privacy evidence.",
                "The evidence package does not demonstrate where data moves, who processes it, how long it is retained, or which protections apply.",
                "Show the data flow, processing purpose, retention period, access boundaries, and contractual safeguards for customer data.",
                "Add data-flow diagram, processing inventory, privacy/security obligations, retention controls, and vendor contractual evidence where applicable.",
                ["GLBA", "Privacy Program Expectations", "NIST Privacy Framework", "ISO 27701"],
                item.title
            ))

    if "sdlc" in text or "devops" in text or "release" in text:
        if "security gate" not in text and "approval" not in text and "change record" not in text:
            findings.append(finding(
                "SDLC Governance Control Gap",
                "Medium",
                "The SDLC/DevOps evidence does not clearly show security gate completion, change approval, or release governance.",
                "The artifact may prove activity occurred, but not that governance requirements were satisfied before production movement.",
                "Where is the evidence that security testing, risk acceptance, and change approval occurred before release?",
                "Map the release to change record, security test results, approval evidence, exception handling, and production deployment record.",
                ["FFIEC Development, Acquisition, and Maintenance", "NIST SSDF", "ISO 27001 Change Management"],
                item.title
            ))

    if "no issue" in text or "green" in text or "effective" in text:
        findings.append(finding(
            "Unsupported Positive Assurance Statement",
            "Low",
            "The artifact includes a positive assurance conclusion but does not provide enough supporting rationale in the provided text.",
            "A conclusion such as effective, green, or no issue should be traceable to test steps and evidence reviewed.",
            "What testing was performed to support the positive conclusion, and who reviewed the result?",
            "Add test procedure, sample basis, evidence references, exception criteria, and reviewer approval.",
            ["FFIEC Audit", "Internal Control Testing Discipline", "CRI Profile Governance"],
            item.title
        ))

    return findings

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Sentinel Assurance Engine", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/sample-cases")
def sample_cases():
    return {"cases": ["IT Metrics Denominator Validation", "Vendor SOC 2 Reliance Review", "Privacy Evidence Challenge", "SDLC Release Governance Review"]}

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    all_findings = []
    for item in payload.items:
        all_findings.extend(analyze_item(item, payload.evidence_type))

    if not all_findings:
        all_findings.append(finding(
            "No Immediate Critical Issue Detected",
            "Low",
            "No rule-based critical issue was detected in the provided text, but the evidence should still be validated for completeness and source lineage.",
            "The current MVP performs deterministic review. Human review is still required for final assurance.",
            "Can management demonstrate source lineage, review approval, and completeness of the submitted evidence?",
            "Retain source extracts, reviewer notes, population basis, and control owner attestation.",
            ["FFIEC Audit", "NIST CSF Govern", "ISO 27001"],
            "Overall Evidence Package"
        ))

    score = max(0, 100 - sum(severity_weight(f["severity"]) for f in all_findings))
    high_risk_count = len([f for f in all_findings if f["severity"] in ["Critical", "High"]])
    rating = "Strong" if score >= 85 else "Moderate" if score >= 65 else "Weak" if score >= 40 else "Critical Attention Required"

    return {
        "product": "Sentinel Assurance Engine",
        "company": "Eye On Bits Pvt Ltd",
        "review_timestamp": datetime.utcnow().isoformat(),
        "organization": payload.organization,
        "industry": payload.industry,
        "evidence_type": payload.evidence_type,
        "review_objective": payload.review_objective,
        "assurance_score": score,
        "overall_rating": rating,
        "high_risk_findings": high_risk_count,
        "total_findings": len(all_findings),
        "executive_summary": f"Sentinel reviewed {len(payload.items)} evidence item(s) and identified {len(all_findings)} examiner-relevant observation(s). The current package is rated '{rating}' with an assurance score of {score}/100.",
        "findings": all_findings
    }
'@ | Out-File -FilePath "backend/app/main.py" -Encoding utf8

@'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'@ | Out-File -FilePath "backend/Dockerfile" -Encoding utf8

@'
{
  "scripts": {
    "dev": "next dev -H 0.0.0.0",
    "build": "next build",
    "start": "next start -H 0.0.0.0"
  },
  "dependencies": {
    "next": "14.2.18",
    "react": "18.3.1",
    "react-dom": "18.3.1"
  },
  "devDependencies": {
    "typescript": "5.6.3",
    "@types/node": "22.10.2",
    "@types/react": "18.3.12",
    "@types/react-dom": "18.3.1"
  }
}
'@ | Out-File -FilePath "frontend/package.json" -Encoding utf8

@'
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
'@ | Out-File -FilePath "frontend/Dockerfile" -Encoding utf8

@'
import "./globals.css";

export const metadata = {
  title: "Sentinel Assurance Platform",
  description: "AI-native assurance intelligence by Eye On Bits"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
'@ | Out-File -FilePath "frontend/app/layout.tsx" -Encoding utf8

@'
"use client";

import { useState } from "react";

const samplePayload = {
  organization: "Sample Tier-1 Bank",
  industry: "BFSI / Regulated Banking",
  evidence_type: "IT Metrics Validation",
  review_objective: "Validate metric evidence for denominator consistency, evidence lineage, and examiner readiness.",
  items: [
    {
      title: "Q4 Phishing Metric Evidence",
      content: "The ITSC deck reported 150 delivered emails. KnowBe4 source export shows denominator changed to 152. Screenshot-only evidence was retained. Metric owner stated the number was corrected later.",
      source_system: "KnowBe4 / ITSC Deck",
      owner: "IT GRC",
      reporting_period: "Q4"
    },
    {
      title: "RCSA Control Effectiveness Metric",
      content: "The reported value was presented as quarterly, but calculation logic appears cumulative year-to-date. The metric narrative says effective and green but does not show test procedure.",
      source_system: "RCSA Tracker",
      owner: "Risk Management",
      reporting_period: "Q3"
    },
    {
      title: "Vendor SOC 2 Evidence",
      content: "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, or CUEC analysis.",
      source_system: "Vendor Portal",
      owner: "TPRM",
      reporting_period: "Annual Review"
    }
  ]
};

export default function Home() {
  const [input, setInput] = useState(JSON.stringify(samplePayload, null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  async function analyze() {
    setError("");
    setResult(null);

    try {
      const payload = JSON.parse(input);
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Backend returned error: " + response.status);
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Eye On Bits Pvt Ltd</p>
          <h1>Sentinel Assurance Platform</h1>
          <p className="subtitle">
            AI-native examiner intelligence for metrics validation, evidence challenge,
            control assurance, and regulatory-ready governance review.
          </p>
        </div>
        <div className="heroCard">
          <span>Sentinel v0.1</span>
          <strong>Metrics & Evidence Examiner</strong>
          <p>Designed for BFSI, audit, GRC, privacy, TPRM, and SDLC assurance workflows.</p>
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Evidence Input</h2>
          <p className="muted">Paste evidence package JSON below. The sample is already loaded.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button onClick={analyze}>Run Examiner Review</button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="panel">
          <h2>Examiner Output</h2>
          {!result && <div className="empty">Run the examiner review to generate assurance score, findings, challenge questions, and remediation guidance.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Assurance Score</span><strong>{result.assurance_score}/100</strong></div>
                <div className="scoreBox"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                <div className="scoreBox"><span>Findings</span><strong>{result.total_findings}</strong></div>
              </div>

              <div className="summary">{result.executive_summary}</div>

              <div className="findings">
                {result.findings.map((finding: any, index: number) => (
                  <div key={index} className="finding">
                    <div className="findingTop">
                      <h3>{finding.title}</h3>
                      <span className={"badge " + finding.severity.toLowerCase()}>{finding.severity}</span>
                    </div>
                    <p><b>Affected item:</b> {finding.affected_item}</p>
                    <p><b>Issue:</b> {finding.issue}</p>
                    <p><b>Evidence gap:</b> {finding.evidence_gap}</p>
                    <p><b>Examiner question:</b> {finding.examiner_question}</p>
                    <p><b>Remediation:</b> {finding.remediation}</p>
                    <div className="frameworks">
                      {finding.framework_relevance.map((fw: string) => <span key={fw}>{fw}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
'@ | Out-File -FilePath "frontend/app/page.tsx" -Encoding utf8

@'
* { box-sizing: border-box; }
body { margin: 0; background: #0b1020; color: #eef2ff; font-family: Arial, Helvetica, sans-serif; }
.page { min-height: 100vh; padding: 32px; }
.hero { display: grid; grid-template-columns: 1.6fr 0.8fr; gap: 24px; align-items: stretch; margin-bottom: 28px; }
.eyebrow { color: #8fb3ff; text-transform: uppercase; letter-spacing: 0.18em; font-size: 12px; font-weight: 700; }
h1 { font-size: 52px; line-height: 1; margin: 12px 0; }
.subtitle { color: #c7d2fe; font-size: 18px; max-width: 900px; }
.heroCard, .panel { background: rgba(255, 255, 255, 0.07); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 24px; padding: 24px; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25); }
.heroCard span { color: #93c5fd; font-size: 13px; }
.heroCard strong { display: block; font-size: 28px; margin: 8px 0; }
.heroCard p { color: #cbd5e1; }
.grid { display: grid; grid-template-columns: 1fr 1.25fr; gap: 24px; }
h2 { margin-top: 0; }
.muted, .empty { color: #aab4d4; }
textarea { width: 100%; min-height: 520px; resize: vertical; border: 1px solid rgba(255, 255, 255, 0.16); background: #050816; color: #dbeafe; border-radius: 18px; padding: 18px; font-family: Consolas, monospace; font-size: 13px; outline: none; }
button { margin-top: 16px; width: 100%; border: 0; border-radius: 16px; padding: 16px 18px; font-weight: 800; cursor: pointer; background: linear-gradient(135deg, #60a5fa, #a78bfa); color: #031026; font-size: 15px; }
.error { margin-top: 14px; color: #fecaca; background: rgba(239, 68, 68, 0.16); padding: 12px; border-radius: 12px; }
.scoreRow { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 18px; }
.scoreBox { background: rgba(15, 23, 42, 0.72); border-radius: 18px; padding: 16px; }
.scoreBox span { display: block; color: #93c5fd; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }
.scoreBox strong { display: block; margin-top: 8px; font-size: 24px; }
.summary { background: rgba(96, 165, 250, 0.12); border-left: 4px solid #60a5fa; padding: 16px; border-radius: 14px; color: #dbeafe; margin-bottom: 18px; }
.finding { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(148, 163, 184, 0.18); border-radius: 20px; padding: 18px; margin-bottom: 16px; }
.findingTop { display: flex; justify-content: space-between; gap: 12px; align-items: center; }
.finding h3 { margin: 0; }
.finding p { color: #cbd5e1; line-height: 1.5; }
.badge { padding: 8px 12px; border-radius: 999px; font-weight: 800; font-size: 12px; }
.badge.high { background: #7f1d1d; color: #fecaca; }
.badge.medium { background: #78350f; color: #fde68a; }
.badge.low { background: #064e3b; color: #bbf7d0; }
.badge.critical { background: #450a0a; color: #fecaca; }
.frameworks { display: flex; flex-wrap: wrap; gap: 8px; }
.frameworks span { background: rgba(96, 165, 250, 0.14); border: 1px solid rgba(96, 165, 250, 0.22); color: #bfdbfe; padding: 7px 10px; border-radius: 999px; font-size: 12px; }
@media (max-width: 980px) { .hero, .grid { grid-template-columns: 1fr; } h1 { font-size: 38px; } }
'@ | Out-File -FilePath "frontend/app/globals.css" -Encoding utf8

@'
version: "3.9"

services:
  backend:
    build:
      context: ./backend
    container_name: sentinel-backend
    ports:
      - "8000:8000"

  frontend:
    build:
      context: ./frontend
    container_name: sentinel-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
'@ | Out-File -FilePath "docker-compose.yml" -Encoding utf8

@'
{
  "organization": "Sample Tier-1 Bank",
  "industry": "BFSI / Regulated Banking",
  "evidence_type": "IT Metrics Validation",
  "review_objective": "Validate metric evidence for denominator consistency, evidence lineage, and examiner readiness.",
  "items": [
    {
      "title": "Q4 Phishing Metric Evidence",
      "content": "The ITSC deck reported 150 delivered emails. KnowBe4 source export shows denominator changed to 152. Screenshot-only evidence was retained. Metric owner stated the number was corrected later.",
      "source_system": "KnowBe4 / ITSC Deck",
      "owner": "IT GRC",
      "reporting_period": "Q4"
    },
    {
      "title": "RCSA Control Effectiveness Metric",
      "content": "The reported value was presented as quarterly, but calculation logic appears cumulative year-to-date. The metric narrative says effective and green but does not show test procedure.",
      "source_system": "RCSA Tracker",
      "owner": "Risk Management",
      "reporting_period": "Q3"
    },
    {
      "title": "Vendor SOC 2 Evidence",
      "content": "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, or CUEC analysis.",
      "source_system": "Vendor Portal",
      "owner": "TPRM",
      "reporting_period": "Annual Review"
    }
  ]
}
'@ | Out-File -FilePath "sample-data/it-metrics-evidence-sample.json" -Encoding utf8

@'
# Sentinel Assurance Platform

AI-native assurance intelligence platform by Eye On Bits Pvt Ltd.

## What Sentinel v0.1 does

Sentinel v0.1 is a Metrics & Evidence Examiner for regulated enterprises. It reviews evidence packages and produces:

- assurance score
- examiner-style findings
- evidence gaps
- challenge questions
- remediation guidance
- framework relevance

## Initial focus

- IT metrics validation
- evidence lineage challenge
- vendor SOC 2 reliance gaps
- privacy evidence gaps
- SDLC governance gaps

## Run locally

```powershell
docker compose up --build
```

Open:

Frontend: http://localhost:3000

Backend health: http://localhost:8000/api/health

## Built by

Eye On Bits Pvt Ltd.
'@ | Out-File -FilePath "README.md" -Encoding utf8

@'
# Sentinel v0.1 Product Thesis

Sentinel is not a generic GRC repository. It is an assurance intelligence layer designed to challenge evidence, metrics, and governance claims the way a strong 2LOD reviewer, internal auditor, or regulator would challenge them.

## First MVP module

Metrics & Evidence Examiner.

## Buyer pain

Regulated organizations often have evidence, but they cannot always prove:

- source lineage
- calculation integrity
- denominator consistency
- reviewer approval
- reporting interpretation
- control operating effectiveness

## Differentiation

Most GRC tools store evidence. Sentinel challenges the evidence.
'@ | Out-File -FilePath "docs/product-thesis.md" -Encoding utf8

@'
__pycache__/
*.pyc
.env
node_modules/
.next/
dist/
build/
.DS_Store
.vscode/
'@ | Out-File -FilePath ".gitignore" -Encoding utf8

Write-Host "Sentinel MVP files created successfully." -ForegroundColor Green
