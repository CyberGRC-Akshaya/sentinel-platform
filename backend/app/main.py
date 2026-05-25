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
