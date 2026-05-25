from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
import html

app = FastAPI(
    title="Sentinel Assurance Engine",
    description="AI-native assurance intelligence engine by Eye On Bits for evidence validation, metric challenge, and examiner-style governance review.",
    version="0.7.0"
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
    return {"Critical": 30, "High": 18, "Medium": 10, "Low": 5}.get(severity, 5)

def finding(title, severity, issue, evidence_gap, examiner_question, remediation, frameworks, affected_item, risk_domain):
    return {
        "title": title,
        "severity": severity,
        "risk_domain": risk_domain,
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

    if "denominator" in text and ("mismatch" in text or "different" in text or "changed" in text or "corrected" in text):
        findings.append(finding(
            "Metric Denominator Inconsistency",
            "High",
            "The metric narrative indicates that the denominator changed or differs across source evidence and reporting output.",
            "The evidence package does not clearly prove population completeness, denominator approval, or reconciliation to source-of-record.",
            "How did management validate that the denominator used in the reported metric is complete, accurate, and consistently applied for the reporting period?",
            "Add source-of-record extract, population logic, reconciliation notes, reviewer approval, and reporting-period tie-out.",
            ["FFIEC Management", "FFIEC Audit", "GLBA 501(b)", "NIST CSF Govern", "CRI Profile Governance"],
            item.title,
            "Metrics Assurance"
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
            item.title,
            "Metrics Assurance"
        ))

    if "screenshot" in text and ("only" in text or "manual" in text):
        findings.append(finding(
            "Weak Evidence Lineage",
            "Medium",
            "The evidence appears to rely heavily on screenshots or manual artifacts without system-of-record lineage.",
            "Screenshots alone may not demonstrate completeness, extraction parameters, source ownership, or calculation integrity.",
            "What source system produced this evidence, who extracted it, and how was completeness validated?",
            "Capture system export, timestamp, extractor identity, query/filter criteria, and independent review evidence.",
            ["FFIEC Audit", "NIST CSF Govern", "ISO 27001 Monitoring and Evidence Expectations"],
            item.title,
            "Evidence Lineage"
        ))

    if "vendor" in text and ("soc 2" in text or "soc2" in text) and ("cuec" not in text):
        findings.append(finding(
            "Incomplete SOC 2 Reliance Analysis",
            "Medium",
            "SOC 2 evidence is referenced but complementary user entity controls are not clearly evaluated.",
            "The review may not prove whether customer-side responsibilities were identified, assigned, and operating.",
            "Which complementary user entity controls apply to the organization, and where is operating evidence retained?",
            "Document CUEC applicability, internal control ownership, evidence location, and residual risk conclusion.",
            ["AICPA SOC 2", "FFIEC Outsourcing Technology Services", "GLBA Vendor Oversight"],
            item.title,
            "Third-Party Risk"
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
                item.title,
                "Privacy / Data Protection"
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
                item.title,
                "SDLC / AI Governance"
            ))

    if "ai" in text and ("approval" not in text or "inventory" not in text or "risk tier" not in text):
        findings.append(finding(
            "AI Governance Approval and Inventory Gap",
            "High",
            "The evidence references AI usage but does not clearly show inventorying, risk classification, approval, or usage restriction logic.",
            "Without traceable AI governance evidence, management cannot demonstrate whether the use case is permitted, reviewed, monitored, or escalated.",
            "Where is the AI use case inventory entry, approval record, classification decision, data handling review, and monitoring plan?",
            "Capture AI inventory record, risk tier, capability classification, data use review, approval authority, monitoring obligations, and incident escalation triggers.",
            ["NIST AI RMF", "ISO/IEC 42001", "FFIEC Information Security Governance Expectations", "Model/AI Risk Governance Good Practice"],
            item.title,
            "SDLC / AI Governance"
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
            item.title,
            "Audit Evidence"
        ))

    return findings

def build_analysis(payload: AnalyzeRequest):
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
            "Overall Evidence Package",
            "General Assurance"
        ))

    score = max(0, 100 - sum(severity_weight(f["severity"]) for f in all_findings))
    high_risk_count = len([f for f in all_findings if f["severity"] in ["Critical", "High"]])

    if score >= 85:
        rating = "Strong"
    elif score >= 65:
        rating = "Moderate"
    elif score >= 40:
        rating = "Weak"
    else:
        rating = "Critical Attention Required"

    severity_counts = {}
    risk_domains = {}
    for f in all_findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1
        risk_domains[f["risk_domain"]] = risk_domains.get(f["risk_domain"], 0) + 1

    top_risk_domains = sorted(
        [{"domain": k, "count": v} for k, v in risk_domains.items()],
        key=lambda x: x["count"],
        reverse=True
    )

    next_steps = [
        "Validate source-of-record evidence and reporting-period tie-out.",
        "Document reviewer approval and management rationale for metric interpretation.",
        "Create remediation owner and target date for high-risk observations.",
        "Retain evidence package, reviewer notes, and updated control mapping for audit traceability."
    ]

    return {
        "product": "Sentinel Assurance Engine",
        "company": "Eye On Bits Pvt Ltd",
        "version": "0.7.0",
        "review_timestamp": datetime.utcnow().isoformat(),
        "organization": payload.organization,
        "industry": payload.industry,
        "evidence_type": payload.evidence_type,
        "review_objective": payload.review_objective,
        "assurance_score": score,
        "overall_rating": rating,
        "high_risk_findings": high_risk_count,
        "total_findings": len(all_findings),
        "severity_distribution": severity_counts,
        "top_risk_domains": top_risk_domains,
        "recommended_next_steps": next_steps,
        "executive_summary": f"Sentinel reviewed {len(payload.items)} evidence item(s) and identified {len(all_findings)} examiner-relevant observation(s). The current package is rated '{rating}' with an assurance score of {score}/100.",
        "findings": all_findings
    }

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Sentinel Assurance Engine", "version": "0.7.0", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    return build_analysis(payload)

@app.post("/api/report-html", response_class=HTMLResponse)
def report_html(payload: AnalyzeRequest):
    result = build_analysis(payload)
    finding_blocks = ""
    for idx, f in enumerate(result["findings"], start=1):
        frameworks = "".join([f"<span class='tag'>{html.escape(x)}</span>" for x in f["framework_relevance"]])
        finding_blocks += f"""
        <div class='finding'>
          <div class='finding-head'>
            <h3>{idx}. {html.escape(f["title"])}</h3>
            <span class='badge {html.escape(f["severity"].lower())}'>{html.escape(f["severity"])}</span>
          </div>
          <p><b>Risk domain:</b> {html.escape(f["risk_domain"])}</p>
          <p><b>Affected item:</b> {html.escape(f["affected_item"])}</p>
          <p><b>Issue:</b> {html.escape(f["issue"])}</p>
          <p><b>Evidence gap:</b> {html.escape(f["evidence_gap"])}</p>
          <p><b>Examiner question:</b> {html.escape(f["examiner_question"])}</p>
          <p><b>Remediation:</b> {html.escape(f["remediation"])}</p>
          <div>{frameworks}</div>
        </div>
        """

    domain_rows = "".join([f"<tr><td>{html.escape(x['domain'])}</td><td>{x['count']}</td></tr>" for x in result["top_risk_domains"]])
    steps = "".join([f"<li>{html.escape(x)}</li>" for x in result["recommended_next_steps"]])

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Examiner Report</title>
<style>
body {{ font-family: Arial, sans-serif; background: #f6f8fb; color: #111827; margin: 0; padding: 32px; }}
.report {{ max-width: 1100px; margin: auto; background: white; border-radius: 18px; padding: 36px; box-shadow: 0 20px 60px rgba(15,23,42,.12); }}
.eyebrow {{ color: #2563eb; text-transform: uppercase; font-size: 12px; font-weight: 700; letter-spacing: .18em; }}
h1 {{ font-size: 40px; margin: 8px 0 4px; }}
.sub {{ color: #4b5563; font-size: 16px; }}
.cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 24px 0; }}
.card {{ border: 1px solid #e5e7eb; border-radius: 14px; padding: 16px; background: #f9fafb; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:22px; margin-top:6px; }}
.summary {{ border-left: 5px solid #2563eb; background: #eff6ff; padding: 16px; border-radius: 12px; margin: 18px 0; }}
.finding {{ border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px; margin: 16px 0; }}
.finding-head {{ display:flex; justify-content:space-between; align-items:center; gap:12px; }}
.finding h3 {{ margin:0; }}
.badge {{ border-radius:999px; padding:7px 11px; color:white; font-size:12px; font-weight:700; }}
.high {{ background:#b91c1c; }} .medium {{ background:#b45309; }} .low {{ background:#047857; }} .critical {{ background:#7f1d1d; }}
.tag {{ display:inline-block; margin:4px 6px 0 0; padding:6px 9px; border-radius:999px; background:#e0ecff; color:#1d4ed8; font-size:12px; }}
table {{ width:100%; border-collapse: collapse; margin-top:12px; }}
td, th {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; }}
.footer {{ margin-top: 28px; color: #6b7280; font-size: 12px; }}
@media print {{ body {{ background:white; padding:0; }} .report {{ box-shadow:none; }} }}
</style>
</head>
<body>
<div class='report'>
<div class='eyebrow'>Eye On Bits Pvt Ltd</div>
<h1>Sentinel Examiner Report</h1>
<div class='sub'>AI-native assurance intelligence for evidence, metrics, control, vendor, privacy, SDLC, and AI governance review.</div>
<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(result["organization"])}</strong></div>
<div class='card'><span>Evidence Type</span><strong>{html.escape(result["evidence_type"])}</strong></div>
<div class='card'><span>Score</span><strong>{result["assurance_score"]}/100</strong></div>
<div class='card'><span>Rating</span><strong>{html.escape(result["overall_rating"])}</strong></div>
</div>
<div class='summary'>{html.escape(result["executive_summary"])}</div>
<h2>Top Risk Domains</h2>
<table><tr><th>Domain</th><th>Finding Count</th></tr>{domain_rows}</table>
<h2>Recommended Next Steps</h2>
<ol>{steps}</ol>
<h2>Examiner Findings</h2>
{finding_blocks}
<div class='footer'>Generated by Sentinel Assurance Engine v0.7. This output supports assurance review and does not replace qualified professional judgment.</div>
</div>
</body>
</html>"""
