# SENTINEL v0.2 PATCH SCRIPT
# Purpose: Upgrade Sentinel v0.1 to v0.2 with sample case library, exportable examiner report, executive dashboard, and richer examiner logic.
# Run from: C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel

$ErrorActionPreference = "Stop"

function Write-NoBom {
    param(
        [string]$Path,
        [string]$Content
    )
    $fullPath = Join-Path (Get-Location) $Path
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($fullPath, $Content, $utf8NoBom)
}

if ((Split-Path -Leaf (Get-Location)) -ne "EyeOnBits-Sentinel") {
    Write-Host "STOP: You are not inside EyeOnBits-Sentinel folder." -ForegroundColor Red
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel" -ForegroundColor Yellow
    exit 1
}

$dirs = @(
"backend",
"backend/app",
"frontend",
"frontend/app",
"docs",
"sample-data",
"reports",
"sales",
"architecture"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$backendMain = @'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import Counter

app = FastAPI(
    title="Sentinel Assurance Engine",
    description="AI-native assurance intelligence engine by Eye On Bits for evidence validation, metric challenge, and examiner-style governance review.",
    version="0.2.0"
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
    return {
        "Critical": 28,
        "High": 17,
        "Medium": 9,
        "Low": 4
    }.get(severity, 4)

def finding(title, severity, domain, issue, evidence_gap, examiner_question, remediation, frameworks, affected_item, buyer_value):
    return {
        "title": title,
        "severity": severity,
        "domain": domain,
        "affected_item": affected_item,
        "issue": issue,
        "evidence_gap": evidence_gap,
        "examiner_question": examiner_question,
        "remediation": remediation,
        "framework_relevance": frameworks,
        "buyer_value": buyer_value
    }

def analyze_item(item: EvidenceItem, evidence_type: str) -> List[Dict[str, Any]]:
    text = f"{item.title} {item.content} {item.source_system or ''} {evidence_type}".lower()
    findings = []

    if "denominator" in text and ("mismatch" in text or "different" in text or "changed" in text or "variance" in text):
        findings.append(finding(
            "Metric Denominator Inconsistency", "High", "IT Metrics Assurance",
            "The metric narrative indicates that the denominator changed or differs across source evidence and reporting output.",
            "The evidence package does not clearly prove population completeness, denominator approval, or reconciliation to source-of-record.",
            "How did management validate that the denominator used in the reported metric is complete, accurate, and consistently applied for the reporting period?",
            "Add source-of-record extract, population logic, reconciliation notes, reviewer approval, and reporting-period tie-out.",
            ["FFIEC Management", "FFIEC Audit", "GLBA 501(b)", "NIST CSF Govern", "CRI Profile Governance"],
            item.title,
            "Prevents executive misreporting and strengthens regulatory defensibility of operational risk metrics."
        ))

    if "cumulative" in text and ("quarter" in text or "quarterly" in text or "periodic" in text):
        findings.append(finding(
            "Cumulative vs Periodic Reporting Logic Risk", "High", "IT Metrics Assurance",
            "The evidence suggests a possible mismatch between cumulative measurement and quarterly reporting interpretation.",
            "The metric definition does not clearly state whether the value is cumulative, point-in-time, rolling-period, or quarter-specific.",
            "Is the metric intended to represent quarterly activity or cumulative year-to-date performance, and how is that interpretation controlled?",
            "Clarify metric definition, align calculation logic to reporting intent, and retain reviewer sign-off for the interpretation.",
            ["FFIEC Management", "FFIEC Audit", "SOX-style reporting discipline", "CRI Profile Risk Measurement"],
            item.title,
            "Helps avoid misleading performance reporting to committees, audit, and senior management."
        ))

    if "screenshot" in text and ("only" in text or "manual" in text or "evidence" in text):
        findings.append(finding(
            "Weak Evidence Lineage", "Medium", "Evidence Integrity",
            "The evidence appears to rely heavily on screenshots or manual artifacts without system-of-record lineage.",
            "Screenshots alone may not demonstrate completeness, extraction parameters, source ownership, or calculation integrity.",
            "What source system produced this evidence, who extracted it, and how was completeness validated?",
            "Capture system export, timestamp, extractor identity, query/filter criteria, and independent review evidence.",
            ["FFIEC Audit", "NIST CSF Govern", "ISO 27001 Monitoring and Measurement"],
            item.title,
            "Improves audit survivability by converting weak artifacts into traceable evidence packages."
        ))

    if "vendor" in text and ("soc 2" in text or "soc2" in text) and ("cuec" not in text):
        findings.append(finding(
            "Incomplete SOC 2 Reliance Analysis", "Medium", "Third Party Risk",
            "SOC 2 evidence is referenced but complementary user entity controls are not clearly evaluated.",
            "The review may not prove whether customer-side responsibilities were identified, assigned, and operating.",
            "Which complementary user entity controls apply to the bank, and where is operating evidence retained?",
            "Document CUEC applicability, internal control ownership, evidence location, and residual risk conclusion.",
            ["AICPA SOC 2", "FFIEC Outsourcing Technology Services", "GLBA Vendor Oversight"],
            item.title,
            "Reduces overreliance on vendor attestations and identifies obligations retained by the customer organization."
        ))

    if ("pii" in text or "npi" in text or "customer data" in text or "personal data" in text) and ("data flow" not in text or "retention" not in text):
        findings.append(finding(
            "Privacy and Data Handling Evidence Gap", "High", "Privacy and Data Protection",
            "The artifact references sensitive customer or personal data but lacks complete data-flow, retention, or contractual privacy evidence.",
            "The evidence package does not fully demonstrate where data moves, who processes it, how long it is retained, or which safeguards apply.",
            "Show the data flow, processing purpose, retention period, access boundaries, and contractual safeguards for customer data.",
            "Add data-flow diagram, processing inventory, privacy/security obligations, retention controls, and vendor contractual evidence where applicable.",
            ["GLBA", "NIST Privacy Framework", "ISO 27701", "Data Protection Governance"],
            item.title,
            "Protects against privacy review gaps, third-party data misuse, and incomplete due diligence."
        ))

    if "sdlc" in text or "devops" in text or "release" in text or "deployment" in text:
        if "security gate" not in text and "approval" not in text and "change record" not in text:
            findings.append(finding(
                "SDLC Governance Control Gap", "Medium", "SDLC and Change Governance",
                "The SDLC/DevOps evidence does not clearly show security gate completion, change approval, or release governance.",
                "The artifact may prove activity occurred, but not that governance requirements were satisfied before production movement.",
                "Where is the evidence that security testing, risk acceptance, and change approval occurred before release?",
                "Map the release to change record, security test results, approval evidence, exception handling, and production deployment record.",
                ["FFIEC Development, Acquisition, and Maintenance", "NIST SSDF", "ISO 27001 Change Management"],
                item.title,
                "Converts engineering activity into auditable release assurance."
            ))

    if ("ai" in text or "model" in text or "copilot" in text or "genai" in text or "agent" in text) and ("approval" not in text or "risk assessment" not in text):
        findings.append(finding(
            "AI Governance Approval Gap", "High", "AI Governance",
            "The evidence references AI usage or AI-enabled capability without clear governance review, approval, or risk assessment evidence.",
            "The package does not demonstrate approved use case, data restrictions, human oversight, monitoring expectations, or exception handling.",
            "Who approved the AI use case, what data may be processed, and how are outputs monitored for risk?",
            "Add AI use-case inventory record, risk tiering, approval evidence, data-use restrictions, monitoring approach, and incident escalation criteria.",
            ["NIST AI RMF", "ISO/IEC 42001", "EU AI Act Concepts", "FFIEC Technology Governance Expectations"],
            item.title,
            "Creates a practical bridge between AI adoption and regulated governance expectations."
        ))

    if ("access" in text or "mfa" in text or "privileged" in text or "iam" in text) and ("recertification" not in text and "approval" not in text):
        findings.append(finding(
            "IAM Evidence Completeness Gap", "Medium", "Identity and Access Management",
            "Access control evidence is referenced but does not demonstrate approval, periodic review, or privileged access oversight.",
            "The evidence may show a configuration or list, but not that access was authorized, reviewed, and appropriate.",
            "Where is the access approval, recertification evidence, and privileged access review trail?",
            "Link access evidence to ticket approval, role mapping, recertification record, privileged access review, and exception handling.",
            ["FFIEC Information Security", "NIST 800-53 AC Controls", "ISO 27001 Access Control"],
            item.title,
            "Improves identity governance defensibility and reduces audit findings around access appropriateness."
        ))

    if "effective" in text or "green" in text or "no issue" in text or "passed" in text:
        if "test procedure" not in text and "sample" not in text and "reviewer" not in text:
            findings.append(finding(
                "Unsupported Positive Assurance Statement", "Low", "Control Testing",
                "The artifact includes a positive assurance conclusion but does not provide enough supporting rationale in the provided text.",
                "A conclusion such as effective, green, no issue, or passed should be traceable to test steps and evidence reviewed.",
                "What testing was performed to support the positive conclusion, and who reviewed the result?",
                "Add test procedure, sample basis, evidence references, exception criteria, and reviewer approval.",
                ["FFIEC Audit", "Internal Control Testing Discipline", "CRI Profile Governance"],
                item.title,
                "Reduces risk of unsupported control effectiveness conclusions."
            ))

    return findings

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Sentinel Assurance Engine",
        "version": "0.2.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/sample-cases")
def sample_cases():
    return {
        "cases": [
            {
                "id": "it_metrics",
                "label": "IT Metrics Examiner",
                "description": "Denominator, evidence lineage, and committee reporting validation.",
                "payload": {
                    "organization": "Sample Tier-1 Bank",
                    "industry": "BFSI / Regulated Banking",
                    "evidence_type": "IT Metrics Validation",
                    "review_objective": "Validate metric evidence for denominator consistency, evidence lineage, and examiner readiness.",
                    "items": [
                        {"title": "Q4 Phishing Metric Evidence", "content": "The ITSC deck reported 150 delivered emails. KnowBe4 source export shows denominator changed to 152. Screenshot-only evidence was retained. Metric owner stated the number was corrected later.", "source_system": "KnowBe4 / ITSC Deck", "owner": "IT GRC", "reporting_period": "Q4"},
                        {"title": "RCSA Control Effectiveness Metric", "content": "The reported value was presented as quarterly, but calculation logic appears cumulative year-to-date. The metric narrative says effective and green but does not show test procedure.", "source_system": "RCSA Tracker", "owner": "Risk Management", "reporting_period": "Q3"}
                    ]
                }
            },
            {
                "id": "vendor_privacy",
                "label": "Vendor & Privacy Examiner",
                "description": "SOC 2 reliance, CUEC, NPI/PII, data-flow, and retention evidence challenge.",
                "payload": {
                    "organization": "Sample Financial Institution",
                    "industry": "BFSI / Third Party Risk",
                    "evidence_type": "Vendor Risk Evidence Review",
                    "review_objective": "Evaluate whether vendor evidence is sufficient for security, privacy, and audit reliance.",
                    "items": [
                        {"title": "Vendor SOC 2 Evidence", "content": "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, or CUEC analysis.", "source_system": "Vendor Portal", "owner": "TPRM", "reporting_period": "Annual Review"},
                        {"title": "Vendor Security Summary", "content": "Vendor says there are no issues and controls are green. Evidence is a manual screenshot only and no reviewer approval is attached.", "source_system": "Vendor Questionnaire", "owner": "Information Security", "reporting_period": "Annual Review"}
                    ]
                }
            },
            {
                "id": "sdlc_ai",
                "label": "SDLC & AI Governance Examiner",
                "description": "Release governance, AI usage approval, security gates, and production-readiness challenge.",
                "payload": {
                    "organization": "Sample Technology Company",
                    "industry": "Enterprise SaaS / AI-enabled product",
                    "evidence_type": "SDLC and AI Governance Review",
                    "review_objective": "Evaluate whether release and AI governance evidence is sufficient for regulated deployment.",
                    "items": [
                        {"title": "AI Assistant Release Evidence", "content": "Engineering deployed a new AI assistant model to production. The release notes reference AI and customer data. No risk assessment or approval record is attached. No security gate is documented.", "source_system": "Jira / CI-CD", "owner": "Product Engineering", "reporting_period": "Release 2.4"},
                        {"title": "Production Deployment Summary", "content": "Deployment completed successfully. The release passed, but there is no change record, no approval evidence, and no test procedure.", "source_system": "DevOps Pipeline", "owner": "DevOps", "reporting_period": "Release 2.4"}
                    ]
                }
            }
        ]
    }

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    all_findings = []

    for item in payload.items:
        all_findings.extend(analyze_item(item, payload.evidence_type))

    if not all_findings:
        all_findings.append(finding(
            "No Immediate Critical Issue Detected", "Low", "General Evidence Review",
            "No rule-based critical issue was detected in the provided text, but the evidence should still be validated for completeness and source lineage.",
            "The current MVP performs deterministic review. Human review is still required for final assurance.",
            "Can management demonstrate source lineage, review approval, and completeness of the submitted evidence?",
            "Retain source extracts, reviewer notes, population basis, and control owner attestation.",
            ["FFIEC Audit", "NIST CSF Govern", "ISO 27001"],
            "Overall Evidence Package",
            "Provides a clean baseline for human-led assurance review."
        ))

    severity_counts = Counter(f["severity"] for f in all_findings)
    domain_counts = Counter(f["domain"] for f in all_findings)

    score = max(0, 100 - sum(severity_weight(f["severity"]) for f in all_findings))
    high_risk_count = len([f for f in all_findings if f["severity"] in ["Critical", "High"]])

    if score >= 85:
        rating = "Strong"
        executive_posture = "Evidence appears directionally strong, subject to validation of source extracts and reviewer approvals."
    elif score >= 65:
        rating = "Moderate"
        executive_posture = "Evidence may be usable, but the package requires additional traceability before executive or audit reliance."
    elif score >= 40:
        rating = "Weak"
        executive_posture = "Evidence is not yet audit-ready. Management should address high-risk evidence gaps before relying on the package."
    else:
        rating = "Critical Attention Required"
        executive_posture = "Evidence has material assurance gaps and should not be relied on without remediation and independent review."

    top_domains = [{"domain": k, "count": v} for k, v in domain_counts.most_common()]

    return {
        "product": "Sentinel Assurance Engine",
        "company": "Eye On Bits Pvt Ltd",
        "version": "0.2.0",
        "review_timestamp": datetime.utcnow().isoformat(),
        "organization": payload.organization,
        "industry": payload.industry,
        "evidence_type": payload.evidence_type,
        "review_objective": payload.review_objective,
        "assurance_score": score,
        "overall_rating": rating,
        "executive_posture": executive_posture,
        "high_risk_findings": high_risk_count,
        "total_findings": len(all_findings),
        "severity_counts": dict(severity_counts),
        "top_domains": top_domains,
        "executive_summary": f"Sentinel reviewed {len(payload.items)} evidence item(s) and identified {len(all_findings)} examiner-relevant observation(s). The current package is rated '{rating}' with an assurance score of {score}/100.",
        "findings": all_findings,
        "recommended_next_steps": [
            "Retain source-of-record exports and extraction parameters.",
            "Document population basis, calculation logic, and reviewer approval.",
            "Map findings to accountable owners and remediation dates.",
            "Prepare examiner-ready rationale for any accepted residual risk."
        ]
    }
'@
Write-NoBom -Path "backend/app/main.py" -Content $backendMain

$frontendPackage = @'
{
  "name": "sentinel-frontend",
  "version": "0.2.0",
  "private": true,
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
'@
Write-NoBom -Path "frontend/package.json" -Content $frontendPackage

$frontendPage = @'
"use client";

import { useEffect, useState } from "react";

const defaultPayload = {
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

type SampleCase = {
  id: string;
  label: string;
  description: string;
  payload: any;
};

export default function Home() {
  const [input, setInput] = useState(JSON.stringify(defaultPayload, null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [samples, setSamples] = useState<SampleCase[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/sample-cases")
      .then((res) => res.json())
      .then((data) => setSamples(data.cases || []))
      .catch(() => setSamples([]));
  }, []);

  function loadSample(sample: SampleCase) {
    setInput(JSON.stringify(sample.payload, null, 2));
    setResult(null);
    setError("");
  }

  async function analyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = JSON.parse(input);
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Backend returned error: " + response.status);

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function downloadReport() {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const stamp = new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-");
    link.href = url;
    link.download = `sentinel-examiner-report-${stamp}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  async function copyExecutiveSummary() {
    if (!result) return;
    const text = [
      "Sentinel Examiner Summary",
      `Organization: ${result.organization}`,
      `Evidence Type: ${result.evidence_type}`,
      `Rating: ${result.overall_rating}`,
      `Assurance Score: ${result.assurance_score}/100`,
      `Findings: ${result.total_findings}`,
      "",
      result.executive_summary,
      "",
      result.executive_posture
    ].join("\n");
    await navigator.clipboard.writeText(text);
    alert("Executive summary copied.");
  }

  const severityOrder = ["Critical", "High", "Medium", "Low"];

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
          <span>Sentinel v0.2</span>
          <strong>Examiner Intelligence Console</strong>
          <p>Built for BFSI, audit, GRC, privacy, TPRM, AI governance, and SDLC assurance workflows.</p>
        </div>
      </section>

      <section className="sampleStrip">
        <div>
          <h2>Sample Case Library</h2>
          <p>Load realistic regulated-industry evidence packages and run examiner review.</p>
        </div>
        <div className="sampleButtons">
          {samples.map((sample) => (
            <button className="sampleBtn" key={sample.id} onClick={() => loadSample(sample)}>
              <strong>{sample.label}</strong>
              <span>{sample.description}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Evidence Input</h2>
          <p className="muted">Paste or load evidence package JSON. Sentinel will challenge evidence quality, metric logic, and governance defensibility.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button className="primaryBtn" onClick={analyze} disabled={loading}>{loading ? "Running Examiner Review..." : "Run Examiner Review"}</button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="panel outputPanel">
          <div className="panelHeader">
            <div>
              <h2>Examiner Output</h2>
              <p className="muted">Executive-ready findings, evidence gaps, challenge questions, and remediation guidance.</p>
            </div>
            {result && (
              <div className="actions">
                <button onClick={downloadReport}>Download JSON</button>
                <button onClick={copyExecutiveSummary}>Copy Summary</button>
                <button onClick={() => window.print()}>Print</button>
              </div>
            )}
          </div>

          {!result && <div className="empty">Run the examiner review to generate assurance score, findings, challenge questions, and remediation guidance.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Assurance Score</span><strong>{result.assurance_score}/100</strong></div>
                <div className="scoreBox"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                <div className="scoreBox"><span>Findings</span><strong>{result.total_findings}</strong></div>
                <div className="scoreBox"><span>High Risk</span><strong>{result.high_risk_findings}</strong></div>
              </div>

              <div className="summary"><b>Executive Summary:</b> {result.executive_summary}<br /><br /><b>Executive Posture:</b> {result.executive_posture}</div>

              <div className="miniGrid">
                <div className="miniPanel">
                  <h3>Severity Distribution</h3>
                  <div className="bars">
                    {severityOrder.map((sev) => {
                      const count = result.severity_counts?.[sev] || 0;
                      return (
                        <div className="barRow" key={sev}>
                          <span>{sev}</span>
                          <div className="barTrack"><div className={`barFill ${sev.toLowerCase()}`} style={{ width: `${Math.min(100, count * 24)}%` }} /></div>
                          <b>{count}</b>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="miniPanel">
                  <h3>Top Risk Domains</h3>
                  {result.top_domains?.map((domain: any) => (
                    <div className="domainRow" key={domain.domain}><span>{domain.domain}</span><b>{domain.count}</b></div>
                  ))}
                </div>
              </div>

              <div className="nextSteps">
                <h3>Recommended Next Steps</h3>
                <ol>{result.recommended_next_steps.map((step: string) => <li key={step}>{step}</li>)}</ol>
              </div>

              <div className="findings">
                {result.findings.map((finding: any, index: number) => (
                  <div key={index} className="finding">
                    <div className="findingTop">
                      <div><h3>{finding.title}</h3><span className="domainTag">{finding.domain}</span></div>
                      <span className={"badge " + finding.severity.toLowerCase()}>{finding.severity}</span>
                    </div>
                    <p><b>Affected item:</b> {finding.affected_item}</p>
                    <p><b>Issue:</b> {finding.issue}</p>
                    <p><b>Evidence gap:</b> {finding.evidence_gap}</p>
                    <p><b>Examiner question:</b> {finding.examiner_question}</p>
                    <p><b>Remediation:</b> {finding.remediation}</p>
                    <p><b>Buyer value:</b> {finding.buyer_value}</p>
                    <div className="frameworks">{finding.framework_relevance.map((fw: string) => <span key={fw}>{fw}</span>)}</div>
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
'@
Write-NoBom -Path "frontend/app/page.tsx" -Content $frontendPage

$frontendCss = @'
* { box-sizing: border-box; }
body { margin: 0; background: radial-gradient(circle at top right, rgba(96,165,250,.18), transparent 32%), radial-gradient(circle at top left, rgba(167,139,250,.12), transparent 28%), #080d1d; color: #eef2ff; font-family: Arial, Helvetica, sans-serif; }
.page { min-height: 100vh; padding: 32px; }
.hero { display: grid; grid-template-columns: 1.6fr .8fr; gap: 24px; align-items: stretch; margin-bottom: 28px; }
.eyebrow { color: #8fb3ff; text-transform: uppercase; letter-spacing: .18em; font-size: 12px; font-weight: 700; }
h1 { font-size: 52px; line-height: 1; margin: 12px 0; }
.subtitle { color: #c7d2fe; font-size: 18px; max-width: 900px; }
.heroCard, .panel, .sampleStrip { background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.12); border-radius: 24px; padding: 24px; box-shadow: 0 24px 80px rgba(0,0,0,.25); }
.heroCard span { color: #93c5fd; font-size: 13px; }
.heroCard strong { display: block; font-size: 28px; margin: 8px 0; }
.heroCard p, .sampleStrip p { color: #cbd5e1; }
.sampleStrip { margin-bottom: 24px; }
.sampleStrip h2 { margin-bottom: 6px; }
.sampleButtons { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 16px; }
.sampleBtn { text-align: left; background: rgba(15,23,42,.82); color: #e0e7ff; border: 1px solid rgba(147,197,253,.2); border-radius: 18px; padding: 16px; cursor: pointer; }
.sampleBtn strong { display: block; margin-bottom: 8px; }
.sampleBtn span { color: #aab4d4; font-size: 13px; line-height: 1.35; }
.grid { display: grid; grid-template-columns: .9fr 1.35fr; gap: 24px; }
h2 { margin-top: 0; }
.muted, .empty { color: #aab4d4; }
textarea { width: 100%; min-height: 560px; resize: vertical; border: 1px solid rgba(255,255,255,.16); background: #050816; color: #dbeafe; border-radius: 18px; padding: 18px; font-family: Consolas, monospace; font-size: 13px; outline: none; }
.primaryBtn { margin-top: 16px; width: 100%; border: 0; border-radius: 16px; padding: 16px 18px; font-weight: 800; cursor: pointer; background: linear-gradient(135deg, #60a5fa, #a78bfa); color: #031026; font-size: 15px; }
.primaryBtn:disabled { opacity: .7; cursor: wait; }
.error { margin-top: 14px; color: #fecaca; background: rgba(239,68,68,.16); padding: 12px; border-radius: 12px; }
.outputPanel { min-height: 680px; }
.panelHeader { display: flex; justify-content: space-between; gap: 18px; align-items: flex-start; }
.actions { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }
.actions button { background: rgba(96,165,250,.14); border: 1px solid rgba(96,165,250,.28); color: #dbeafe; border-radius: 999px; padding: 10px 12px; cursor: pointer; font-weight: 700; }
.scoreRow { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }
.scoreBox, .miniPanel { background: rgba(15,23,42,.72); border-radius: 18px; padding: 16px; }
.scoreBox span { display: block; color: #93c5fd; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
.scoreBox strong { display: block; margin-top: 8px; font-size: 24px; }
.summary { background: rgba(96,165,250,.12); border-left: 4px solid #60a5fa; padding: 16px; border-radius: 14px; color: #dbeafe; margin-bottom: 18px; line-height: 1.45; }
.miniGrid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 18px; }
.miniPanel h3 { margin-top: 0; }
.barRow { display: grid; grid-template-columns: 80px 1fr 28px; gap: 10px; align-items: center; margin: 10px 0; color: #cbd5e1; }
.barTrack { background: rgba(255,255,255,.08); border-radius: 999px; height: 10px; overflow: hidden; }
.barFill { height: 10px; border-radius: 999px; }
.barFill.critical, .barFill.high { background: #ef4444; }
.barFill.medium { background: #f59e0b; }
.barFill.low { background: #10b981; }
.domainRow { display: flex; justify-content: space-between; padding: 11px 0; border-bottom: 1px solid rgba(255,255,255,.08); color: #cbd5e1; }
.nextSteps { background: rgba(16,185,129,.10); border: 1px solid rgba(16,185,129,.20); border-radius: 18px; padding: 16px; margin-bottom: 18px; }
.nextSteps h3 { margin-top: 0; }
.nextSteps li { color: #d1fae5; margin-bottom: 8px; }
.finding { background: rgba(15,23,42,.8); border: 1px solid rgba(148,163,184,.18); border-radius: 20px; padding: 18px; margin-bottom: 16px; }
.findingTop { display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }
.finding h3 { margin: 0 0 8px 0; }
.finding p { color: #cbd5e1; line-height: 1.5; }
.domainTag { color: #bfdbfe; background: rgba(96,165,250,.13); border-radius: 999px; padding: 7px 10px; font-size: 12px; }
.badge { padding: 8px 12px; border-radius: 999px; font-weight: 800; font-size: 12px; }
.badge.high { background: #7f1d1d; color: #fecaca; }
.badge.medium { background: #78350f; color: #fde68a; }
.badge.low { background: #064e3b; color: #bbf7d0; }
.badge.critical { background: #450a0a; color: #fecaca; }
.frameworks { display: flex; flex-wrap: wrap; gap: 8px; }
.frameworks span { background: rgba(96,165,250,.14); border: 1px solid rgba(96,165,250,.22); color: #bfdbfe; padding: 7px 10px; border-radius: 999px; font-size: 12px; }
@media print { body { background: white; color: black; } .panel, .heroCard, .sampleStrip, .finding, .summary, .miniPanel, .nextSteps { box-shadow: none; border: 1px solid #ddd; background: white; color: black; } .grid { display: block; } .panel:first-child, .sampleStrip, .actions, textarea, .primaryBtn { display: none; } p, li, .muted, .finding p { color: black; } }
@media (max-width: 1100px) { .hero, .grid, .sampleButtons, .miniGrid { grid-template-columns: 1fr; } .scoreRow { grid-template-columns: repeat(2, 1fr); } h1 { font-size: 38px; } }
'@
Write-NoBom -Path "frontend/app/globals.css" -Content $frontendCss

$dockerCompose = @'
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
'@
Write-NoBom -Path "docker-compose.yml" -Content $dockerCompose

$readme = @'
# Sentinel Assurance Platform

AI-native assurance intelligence platform by Eye On Bits Pvt Ltd.

## Sentinel v0.2

Sentinel v0.2 is an Examiner Intelligence Console for regulated enterprises. It reviews evidence packages and produces:

- assurance score
- executive posture
- examiner-style findings
- evidence gaps
- challenge questions
- remediation guidance
- severity distribution
- risk-domain summary
- framework relevance
- downloadable examiner report

## Initial focus

- IT metrics validation
- evidence lineage challenge
- vendor SOC 2 reliance gaps
- privacy evidence gaps
- SDLC governance gaps
- AI governance approval gaps
- IAM evidence completeness gaps

## Run locally

```powershell
docker compose up --build
```

Open:

```text
Frontend: http://localhost:3000
Backend health: http://localhost:8000/api/health
```

## Built by

Eye On Bits Pvt Ltd.
'@
Write-NoBom -Path "README.md" -Content $readme

$productThesis = @'
# Sentinel v0.2 Product Thesis

Sentinel is not a generic GRC repository. It is an assurance intelligence layer designed to challenge evidence, metrics, and governance claims the way a strong 2LOD reviewer, internal auditor, or regulator would challenge them.

## First MVP module

Examiner Intelligence Console.

## Buyer pain

Regulated organizations often have evidence, but they cannot always prove:

- source lineage
- calculation integrity
- denominator consistency
- reviewer approval
- reporting interpretation
- control operating effectiveness
- SOC 2 reliance boundaries
- privacy/data-flow completeness
- SDLC release governance
- AI use-case approval and monitoring

## Differentiation

Most GRC tools store evidence. Sentinel challenges the evidence.

## Commercial use

Sentinel can support consulting-assisted services such as:

- IT metrics assurance review
- TPRM evidence challenge
- AI governance readiness review
- SDLC governance review
- privacy/data-handling evidence assessment
'@
Write-NoBom -Path "docs/product-thesis.md" -Content $productThesis

Write-Host ""
Write-Host "Sentinel v0.2 patch applied successfully." -ForegroundColor Green
Write-Host "Next command: docker compose down --remove-orphans" -ForegroundColor Yellow
Write-Host "Then: docker compose build --no-cache" -ForegroundColor Yellow
Write-Host "Then: docker compose up" -ForegroundColor Yellow
