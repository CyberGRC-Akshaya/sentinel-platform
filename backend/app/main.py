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