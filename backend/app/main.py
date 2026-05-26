
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path
import html
import json
import sqlite3
import uuid

DB_PATH = Path("data/sentinel.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Sentinel Evidence Defensibility Workbench",
    description="Professional assurance workbench with review vault, portfolio analytics, control atlas mapping, evidence request workflow, demo-room storytelling, board-pack generation, remediation register, and executive reporting exports.",
    version="10.1.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONTROL_ATLAS = {
    "Metrics Assurance": [
        {
            "control_id": "SEN-MET-01",
            "control_theme": "Metric Source Lineage",
            "control_objective": "Metrics used for governance reporting should be traceable to approved source systems and retained supporting evidence.",
            "expected_evidence": ["source-of-record export", "query/filter criteria", "timestamped report", "evidence owner confirmation", "review approval"],
            "challenge_questions": [
                "What system is the source of record for this metric?",
                "Can the reported value be reconciled to the exported population?",
                "Was the metric reviewed before committee reporting?"
            ],
            "mapped_frameworks": ["FFIEC-style Management/Audit Expectations", "NIST CSF Govern", "Audit Evidence Discipline"]
        },
        {
            "control_id": "SEN-MET-02",
            "control_theme": "Metric Calculation Integrity",
            "control_objective": "Metric numerator, denominator, formula, reporting period, and adjustment logic should be documented and consistently applied.",
            "expected_evidence": ["metric definition", "formula", "numerator support", "denominator support", "recalculation evidence", "reporting-period tie-out"],
            "challenge_questions": [
                "Is the calculation quarterly, monthly, point-in-time, or cumulative?",
                "Are exclusions and manual adjustments approved?",
                "Does the committee deck match the system-of-record value?"
            ],
            "mapped_frameworks": ["FFIEC-style Management/Audit Expectations", "NIST CSF Govern"]
        }
    ],
    "Third-Party Risk": [
        {
            "control_id": "SEN-TPR-01",
            "control_theme": "SOC 2 Reliance and CUEC Review",
            "control_objective": "SOC 2 reliance should include scope validation, exception review, subservice organization consideration, and CUEC applicability analysis.",
            "expected_evidence": ["SOC 2 Type II report", "bridge letter if applicable", "CUEC analysis", "subservice organization review", "exception review", "residual risk conclusion"],
            "challenge_questions": [
                "Does the SOC 2 period cover the reliance period?",
                "Were CUECs mapped to internal responsibilities?",
                "Were exceptions reviewed for residual risk?"
            ],
            "mapped_frameworks": ["AICPA SOC 2", "FFIEC Third-Party / Outsourcing Expectations"]
        },
        {
            "control_id": "SEN-TPR-02",
            "control_theme": "Vendor Data Handling Boundary",
            "control_objective": "Vendor evidence should demonstrate customer data flow, retention, access boundaries, transfer methods, and security/privacy obligations.",
            "expected_evidence": ["data-flow diagram", "retention description", "security addendum", "DPA or privacy obligations", "access controls", "destruction evidence"],
            "challenge_questions": [
                "What customer or regulated data does the vendor process?",
                "Where is the data stored and transferred?",
                "How are retention and deletion obligations evidenced?"
            ],
            "mapped_frameworks": ["GLBA Customer Information Safeguards Relevance", "FFIEC Third-Party / Outsourcing Expectations"]
        }
    ],
    "Privacy / Data Protection": [
        {
            "control_id": "SEN-PRI-01",
            "control_theme": "Customer Information Handling",
            "control_objective": "Evidence packages involving customer information should identify processing purpose, data categories, access boundaries, retention, and disposal expectations.",
            "expected_evidence": ["processing purpose", "data-flow diagram", "data category inventory", "retention schedule", "access list", "deletion/destruction evidence"],
            "challenge_questions": [
                "What customer information is processed?",
                "Who can access it and why?",
                "How is retention and destruction demonstrated?"
            ],
            "mapped_frameworks": ["GLBA Customer Information Safeguards Relevance", "NIST Privacy Framework / ISO 27701 Relevance"]
        }
    ],
    "SDLC / Change / DevSecOps": [
        {
            "control_id": "SEN-SDL-01",
            "control_theme": "Release Governance Evidence",
            "control_objective": "Production releases should have change approval, security testing, implementation evidence, and rollback or contingency planning.",
            "expected_evidence": ["change record", "release approval", "security testing", "deployment evidence", "rollback plan", "risk acceptance if applicable"],
            "challenge_questions": [
                "Was the release approved before production deployment?",
                "Were security gates completed or risk-accepted?",
                "Is rollback evidence available?"
            ],
            "mapped_frameworks": ["FFIEC Development, Acquisition, and Maintenance", "NIST SSDF / Secure SDLC Good Practice"]
        }
    ],
    "AI Governance": [
        {
            "control_id": "SEN-AI-01",
            "control_theme": "AI Use Case Governance",
            "control_objective": "AI-enabled use cases should have inventory, ownership, intended use, risk classification, approval, monitoring, and incident escalation evidence.",
            "expected_evidence": ["AI inventory entry", "use case owner", "risk tier", "approval record", "data review", "monitoring plan", "incident escalation criteria"],
            "challenge_questions": [
                "Is the AI use case formally inventoried?",
                "Who owns the model or AI-enabled functionality?",
                "What monitoring and escalation evidence exists?"
            ],
            "mapped_frameworks": ["NIST AI RMF", "ISO/IEC 42001"]
        }
    ],
    "Identity & Access": [
        {
            "control_id": "SEN-IAM-01",
            "control_theme": "Access Governance Evidence",
            "control_objective": "Access evidence should demonstrate request, approval, authentication control, periodic review, exception management, and revocation where applicable.",
            "expected_evidence": ["access request", "approval", "MFA/risk decision evidence", "access review", "exception register", "revocation evidence"],
            "challenge_questions": [
                "Who approved the access and based on what business need?",
                "Was MFA or compensating control evidence available?",
                "Were exceptions tracked and reviewed?"
            ],
            "mapped_frameworks": ["FFIEC Authentication / Access Governance Expectations", "ISO 27001 Access Control"]
        }
    ],
    "General Evidence Defensibility": [
        {
            "control_id": "SEN-GEN-01",
            "control_theme": "Evidence Reliability and Sufficiency",
            "control_objective": "Evidence should be sufficient, reliable, relevant, retained, reviewed, and directly tied to the claim being supported.",
            "expected_evidence": ["evidence objective", "source", "owner", "evidence date", "review trail", "control linkage"],
            "challenge_questions": [
                "What claim does this evidence support?",
                "Who owns and reviewed it?",
                "Is the evidence reliable enough for audit reliance?"
            ],
            "mapped_frameworks": ["Audit Evidence Discipline"]
        }
    ]
}

FRAMEWORK_LIBRARY = {
    "Metrics Assurance": [
        {
            "framework": "FFIEC-style Management / Audit Expectations",
            "mapping_type": "Examiner-style assurance relevance",
            "rationale": "Management reporting and control metrics should be supported by source data, calculation logic, period alignment, and review evidence.",
            "evidence_expected": "Metric definition, source export, numerator, denominator, reconciliation, reviewer approval, and committee tie-out."
        },
        {
            "framework": "NIST CSF Govern",
            "mapping_type": "Governance relevance",
            "rationale": "Governance outcomes require measurement, accountability, and evidence-based oversight.",
            "evidence_expected": "Risk reporting, control monitoring, accountable owner review, and escalation evidence."
        }
    ],
    "Third-Party Risk": [
        {
            "framework": "AICPA SOC 2",
            "mapping_type": "Assurance reliance relevance",
            "rationale": "SOC 2 reliance requires understanding scope, exceptions, system boundaries, and CUECs.",
            "evidence_expected": "SOC 2 report, bridge letter, CUEC analysis, subservice review, and residual risk conclusion."
        },
        {
            "framework": "FFIEC Third-Party / Outsourcing Expectations",
            "mapping_type": "Third-party oversight relevance",
            "rationale": "Outsourced technology risk should be evaluated through due diligence, contractual safeguards, monitoring, and issue tracking.",
            "evidence_expected": "Vendor risk assessment, contract terms, data-flow evidence, monitoring artifacts, and issue log."
        }
    ],
    "Privacy / Data Protection": [
        {
            "framework": "GLBA Customer Information Safeguards Relevance",
            "mapping_type": "Data protection relevance",
            "rationale": "Customer information handling should be supported by safeguards, access boundaries, retention controls, and third-party oversight.",
            "evidence_expected": "Data-flow diagram, processing purpose, access list, retention/destruction evidence, and privacy/security obligations."
        }
    ],
    "SDLC / Change / DevSecOps": [
        {
            "framework": "FFIEC Development, Acquisition, and Maintenance",
            "mapping_type": "Technology governance relevance",
            "rationale": "Development and release activities should be governed, tested, approved, risk-assessed, and controlled before production movement.",
            "evidence_expected": "Change record, release approval, security testing, risk acceptance, deployment record, and rollback evidence."
        },
        {
            "framework": "NIST SSDF / Secure SDLC Good Practice",
            "mapping_type": "Secure development relevance",
            "rationale": "Secure development requires evidence of security testing, vulnerability handling, and release integrity.",
            "evidence_expected": "SAST/DAST/pentest evidence, vulnerability disposition, release review, and approval gate evidence."
        }
    ],
    "AI Governance": [
        {
            "framework": "NIST AI RMF",
            "mapping_type": "AI risk governance relevance",
            "rationale": "AI systems should be governed, mapped, measured, and managed based on intended use, risk, and monitoring obligations.",
            "evidence_expected": "AI inventory, risk tier, data review, monitoring plan, approval record, and incident escalation criteria."
        },
        {
            "framework": "ISO/IEC 42001",
            "mapping_type": "AI management system relevance",
            "rationale": "AI governance should be supported by accountable management practices, documented roles, risk treatment, and monitoring evidence.",
            "evidence_expected": "AI management roles, policy/standard evidence, risk treatment records, use case approvals, and monitoring evidence."
        }
    ],
    "Identity & Access": [
        {
            "framework": "FFIEC Authentication / Access Governance Expectations",
            "mapping_type": "Access control relevance",
            "rationale": "Access and authentication controls should be risk-based, approved, reviewed, monitored, and supported by exception evidence.",
            "evidence_expected": "Access request, approval, MFA/risk decision evidence, access review, exception register, and revocation evidence."
        }
    ],
    "General Evidence Defensibility": [
        {
            "framework": "Audit Evidence Discipline",
            "mapping_type": "Professional assurance relevance",
            "rationale": "Evidence should be sufficient, reliable, relevant, retained, reviewed, and tied to the claim being supported.",
            "evidence_expected": "Evidence objective, source, owner, date, review trail, conclusion, and linkage to control or risk statement."
        }
    ]
}

DIMENSIONS = [
    {"key": "source_lineage", "label": "Source Lineage", "weight": 18, "positive": ["source export", "system export", "source-of-record", "source of record", "query", "extract", "timestamp", "api export"], "negative": ["screenshot-only", "screenshot only", "manual", "email screenshot", "corrected later"]},
    {"key": "completeness", "label": "Completeness", "weight": 16, "positive": ["population", "complete", "full extract", "all records", "reconciliation", "tie-out", "scope boundary"], "negative": ["partial", "sample only", "not included", "missing", "not available", "does not include", "not provided"]},
    {"key": "calculation_integrity", "label": "Calculation Integrity", "weight": 16, "positive": ["numerator", "denominator", "formula", "calculation", "logic", "recalculation", "validated"], "negative": ["changed to", "mismatch", "inconsistent", "corrected later", "cumulative", "unclear", "manual adjustment"]},
    {"key": "review_approval", "label": "Review & Approval Evidence", "weight": 14, "positive": ["approved", "reviewed", "sign-off", "sign off", "attested", "owner approval", "review notes"], "negative": ["no approval", "not approved", "no review", "review not shown", "owner stated", "verbal confirmation"]},
    {"key": "period_alignment", "label": "Reporting Period Alignment", "weight": 12, "positive": ["q1", "q2", "q3", "q4", "monthly", "quarterly", "annual", "reporting period", "as of", "period end"], "negative": ["year-to-date", "ytd", "cumulative", "prior period", "unclear period", "mixed period"]},
    {"key": "governance_traceability", "label": "Governance Traceability", "weight": 14, "positive": ["policy", "standard", "control", "risk acceptance", "exception", "issue", "ticket", "change record", "jira", "servicenow"], "negative": ["no ticket", "no change record", "no exception", "no risk acceptance", "not documented"]},
    {"key": "data_handling", "label": "Data Handling & Privacy Boundary", "weight": 10, "positive": ["data flow", "retention", "pii", "npi", "customer data", "encryption", "access boundary", "dpa", "deletion"], "negative": ["no data flow", "retention not", "unknown retention", "no dpa", "unknown processing"]}
]

INTAKE_REQUIREMENTS = {
    "Metrics Assurance": ["metric definition", "source export", "numerator", "denominator", "reporting period", "review approval", "reconciliation"],
    "Third-Party Risk": ["soc 2", "cuec", "bridge letter", "subservice", "data flow", "contract", "residual risk"],
    "Privacy / Data Protection": ["data flow", "processing purpose", "retention", "access boundary", "privacy review", "deletion", "dpa"],
    "SDLC / Change / DevSecOps": ["change record", "release approval", "security testing", "risk acceptance", "deployment evidence", "rollback"],
    "AI Governance": ["ai inventory", "risk tier", "approval", "data review", "monitoring plan", "incident escalation", "owner"],
    "Identity & Access": ["access approval", "mfa evidence", "access review", "exception", "revocation", "privileged access"],
    "General Evidence Defensibility": ["source", "owner", "review", "approval", "control objective", "evidence date"]
}

DOMAIN_KEYWORDS = [
    ("AI Governance", [" ai ", "genai", "model", "prompt", "copilot", "assistant", "machine learning", "risk tier"]),
    ("Identity & Access", ["iam", "access", "authentication", "mfa", "privileged", "password", "entitlement"]),
    ("Third-Party Risk", ["vendor", "soc 2", "soc2", "cuec", "subservice", "supplier", "outsourc"]),
    ("Privacy / Data Protection", ["pii", "npi", "customer data", "data flow", "retention", "privacy", "dpa", "deletion"]),
    ("SDLC / Change / DevSecOps", ["sdlc", "devops", "release", "change record", "deployment", "security testing", "sast", "dast"]),
    ("Metrics Assurance", ["metric", "denominator", "numerator", "committee", "dashboard", "scorecard", "rcsa"])
]

class EvidenceItem(BaseModel):
    title: str
    content: str
    source_system: Optional[str] = None
    owner: Optional[str] = None
    reporting_period: Optional[str] = None
    artifact_type: Optional[str] = None
    evidence_date: Optional[str] = None
    control_reference: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class AnalyzeRequest(BaseModel):
    organization: str
    industry: str
    evidence_type: str
    review_objective: str
    items: List[EvidenceItem]

class RegisterUpdate(BaseModel):
    rows: List[Dict[str, Any]]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                organization TEXT,
                industry TEXT,
                evidence_type TEXT,
                review_objective TEXT,
                overall_rating TEXT,
                evidence_defensibility_score INTEGER,
                intake_coverage_score INTEGER,
                metadata_completeness_score INTEGER,
                total_findings INTEGER,
                payload_json TEXT NOT NULL,
                result_json TEXT NOT NULL,
                register_json TEXT NOT NULL
            )
        """)
        conn.commit()

@app.on_event("startup")
def startup():
    ensure_db()

def normalize_text(item: EvidenceItem) -> str:
    return f" {item.title} {item.content} {item.source_system or ''} {item.owner or ''} {item.reporting_period or ''} {item.artifact_type or ''} {item.control_reference or ''} ".lower()

def detect_domain(text: str) -> str:
    for domain, keywords in DOMAIN_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return domain
    return "General Evidence Defensibility"

def infer_artifact_profile(item: EvidenceItem, domain: str) -> Dict[str, Any]:
    text = normalize_text(item)
    artifact_type = item.artifact_type or "Unspecified Evidence Artifact"
    if "screenshot" in text:
        artifact_type = "Screenshot / Visual Evidence"
    elif "soc 2" in text or "soc2" in text:
        artifact_type = "SOC 2 / Vendor Assurance"
    elif "metric" in text or "denominator" in text:
        artifact_type = "Metric Evidence"
    elif "change record" in text or "release" in text:
        artifact_type = "Change / Release Evidence"
    elif "access" in text or "mfa" in text:
        artifact_type = "IAM / Access Evidence"
    elif "ai " in text or "risk tier" in text:
        artifact_type = "AI Governance Evidence"

    profile = {
        "title": item.title, "domain": domain, "artifact_type": artifact_type,
        "has_owner": bool(item.owner), "has_source_system": bool(item.source_system),
        "has_reporting_period": bool(item.reporting_period), "has_control_reference": bool(item.control_reference),
        "has_evidence_date": bool(item.evidence_date), "text_length": len(item.content or ""),
        "metadata_completeness_score": 0, "missing_metadata": []
    }
    checks = [("has_owner", "owner"), ("has_source_system", "source_system"), ("has_reporting_period", "reporting_period"), ("has_control_reference", "control_reference"), ("has_evidence_date", "evidence_date")]
    present = 0
    for key, label in checks:
        if profile[key]:
            present += 1
        else:
            profile["missing_metadata"].append(label)
    profile["metadata_completeness_score"] = round((present / len(checks)) * 100)
    return profile

def intake_gap_analysis(item: EvidenceItem, domain: str) -> Dict[str, Any]:
    text = normalize_text(item)
    requirements = INTAKE_REQUIREMENTS.get(domain, INTAKE_REQUIREMENTS["General Evidence Defensibility"])
    present, missing = [], []
    for requirement in requirements:
        if requirement.lower() in text:
            present.append(requirement)
        else:
            missing.append(requirement)
    coverage = round((len(present) / len(requirements)) * 100) if requirements else 0
    rating = "Strong Intake" if coverage >= 80 else "Partial Intake" if coverage >= 55 else "Weak Intake"
    return {"title": item.title, "domain": domain, "required_evidence_elements": requirements, "present_elements": present, "missing_elements": missing, "intake_coverage_score": coverage, "intake_rating": rating}

def dimension_score(text: str, dimension: Dict[str, Any]) -> Dict[str, Any]:
    positive_hits = [p for p in dimension["positive"] if p in text]
    negative_hits = [n for n in dimension["negative"] if n in text]
    score = max(0, min(100, 65 + (len(positive_hits) * 8) - (len(negative_hits) * 12)))
    rating = "Strong" if score >= 80 else "Moderate" if score >= 60 else "Weak" if score >= 40 else "Deficient"
    return {"key": dimension["key"], "label": dimension["label"], "weight": dimension["weight"], "score": score, "rating": rating, "positive_indicators": positive_hits, "negative_indicators": negative_hits}

def map_control_atlas(domain: str, text: str) -> Dict[str, Any]:
    controls = CONTROL_ATLAS.get(domain, CONTROL_ATLAS["General Evidence Defensibility"])
    mapped_controls = []
    all_expected = []
    all_questions = []

    for control in controls:
        expected = control.get("expected_evidence", [])
        present = [e for e in expected if e.lower() in text]
        missing = [e for e in expected if e.lower() not in text]
        coverage = round((len(present) / len(expected)) * 100) if expected else 0
        mapped_controls.append({
            **control,
            "present_evidence": present,
            "missing_evidence": missing,
            "control_coverage_score": coverage,
            "control_rating": "Strong" if coverage >= 80 else "Partial" if coverage >= 50 else "Weak"
        })
        all_expected.extend(missing)
        all_questions.extend(control.get("challenge_questions", []))

    avg_coverage = round(sum(c["control_coverage_score"] for c in mapped_controls) / len(mapped_controls)) if mapped_controls else 0
    return {
        "domain": domain,
        "control_coverage_score": avg_coverage,
        "mapped_controls": mapped_controls,
        "missing_evidence_summary": sorted(list(set(all_expected))),
        "challenge_question_bank": sorted(list(set(all_questions)))
    }

def score_item(item: EvidenceItem) -> Dict[str, Any]:
    text = normalize_text(item)
    domain = detect_domain(text)
    dimensions = [dimension_score(text, d) for d in DIMENSIONS]
    weighted_total = sum(d["score"] * d["weight"] for d in dimensions)
    total_weight = sum(d["weight"] for d in dimensions)
    score = round(weighted_total / total_weight)
    rating = "Strong" if score >= 85 else "Moderate" if score >= 70 else "Weak" if score >= 50 else "Critical Attention Required"
    return {
        "item_title": item.title,
        "domain": domain,
        "score": score,
        "rating": rating,
        "dimensions": dimensions,
        "intake_gap_analysis": intake_gap_analysis(item, domain),
        "artifact_profile": infer_artifact_profile(item, domain),
        "control_atlas_mapping": map_control_atlas(domain, text)
    }

def severity_from_score(score: int) -> str:
    if score < 40:
        return "Critical"
    if score < 55:
        return "High"
    if score < 70:
        return "Medium"
    return "Low"

def framework_mappings_for(domain: str) -> List[Dict[str, str]]:
    return FRAMEWORK_LIBRARY.get(domain, FRAMEWORK_LIBRARY["General Evidence Defensibility"])

def build_finding(item: EvidenceItem, item_score: Dict[str, Any], dimension: Dict[str, Any], idx: int) -> Dict[str, Any]:
    domain = item_score["domain"]
    severity = severity_from_score(dimension["score"])
    negative = ", ".join(dimension.get("negative_indicators", [])) or "insufficient positive evidence indicators"
    positive = ", ".join(dimension.get("positive_indicators", [])) or "limited traceable evidence"
    control_map = item_score.get("control_atlas_mapping", {})
    mapped_ids = [c["control_id"] for c in control_map.get("mapped_controls", [])]
    request = {
        "request_id": f"REQ-{idx:03d}",
        "evidence_needed": f"Provide evidence supporting {dimension['label'].lower()} for {item.title}.",
        "preferred_artifacts": control_map.get("missing_evidence_summary", [])[:8] or ["supporting evidence package"],
        "owner": item.owner or "Evidence Owner",
        "priority": severity,
        "status": "Open"
    }
    return {
        "finding_id": f"SEN-{idx:03d}",
        "title": f"{dimension['label']} Defensibility Gap",
        "severity": severity,
        "severity_rationale": f"{dimension['label']} scored {dimension['score']}/100 and is rated {dimension['rating']} based on negative indicators ({negative}) and positive indicators ({positive}).",
        "risk_domain": domain,
        "affected_item": item.title,
        "dimension": dimension["label"],
        "issue": f"{dimension['label']} is not sufficiently evidenced for this review item.",
        "evidence_gap": f"The submitted evidence does not sufficiently demonstrate {dimension['label'].lower()} for the claim being reviewed.",
        "examiner_question": f"What evidence proves {dimension['label'].lower()} for '{item.title}', and who reviewed or approved that evidence?",
        "remediation": f"Provide traceable evidence and management review support for {dimension['label'].lower()}.",
        "framework_relevance": [m["framework"] for m in framework_mappings_for(domain)],
        "framework_mappings": framework_mappings_for(domain),
        "control_atlas_ids": mapped_ids,
        "evidence_request": request,
        "management_response": "",
        "status": "Open"
    }

def build_register(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for finding in result.get("findings", []):
        request = finding.get("evidence_request", {})
        rows.append({
            "finding_id": finding.get("finding_id"),
            "severity": finding.get("severity"),
            "risk_domain": finding.get("risk_domain"),
            "control_atlas_ids": "; ".join(finding.get("control_atlas_ids", [])),
            "affected_item": finding.get("affected_item"),
            "issue": finding.get("issue"),
            "remediation": finding.get("remediation"),
            "evidence_needed": request.get("evidence_needed", ""),
            "preferred_artifacts": "; ".join(request.get("preferred_artifacts", [])),
            "owner": request.get("owner", ""),
            "target_date": "",
            "status": "Open",
            "management_response": "",
            "closure_evidence": "",
            "validation_notes": ""
        })
    return rows

def build_analysis(payload: AnalyzeRequest) -> Dict[str, Any]:
    item_scores = [score_item(item) for item in payload.items]
    findings = []
    request_counter = 1

    for item, item_score in zip(payload.items, item_scores):
        weak_dimensions = [d for d in item_score["dimensions"] if d["score"] < 70 or d["negative_indicators"]]
        weak_dimensions = sorted(weak_dimensions, key=lambda d: d["score"])[:4]
        for dim in weak_dimensions:
            findings.append(build_finding(item, item_score, dim, request_counter))
            request_counter += 1

        intake = item_score["intake_gap_analysis"]
        if intake["intake_coverage_score"] < 55:
            domain = item_score["domain"]
            control_map = item_score.get("control_atlas_mapping", {})
            findings.append({
                "finding_id": f"SEN-{request_counter:03d}",
                "title": "Evidence Intake Coverage Gap",
                "severity": "Medium",
                "severity_rationale": f"Required evidence element coverage is {intake['intake_coverage_score']}/100 and rated {intake['intake_rating']}.",
                "risk_domain": domain,
                "affected_item": item.title,
                "dimension": "Evidence Intake Completeness",
                "issue": "The package is missing expected evidence elements for the detected review domain.",
                "evidence_gap": "Missing elements: " + ", ".join(intake["missing_elements"]),
                "examiner_question": "Which missing evidence elements are unavailable, not applicable, or retained in a separate system?",
                "remediation": "Provide missing evidence elements or document why they are not applicable.",
                "framework_relevance": [m["framework"] for m in framework_mappings_for(domain)],
                "framework_mappings": framework_mappings_for(domain),
                "control_atlas_ids": [c["control_id"] for c in control_map.get("mapped_controls", [])],
                "evidence_request": {
                    "request_id": f"REQ-{request_counter:03d}",
                    "evidence_needed": "Provide missing expected evidence elements: " + ", ".join(intake["missing_elements"]),
                    "preferred_artifacts": intake["missing_elements"],
                    "owner": item.owner or "Evidence Owner",
                    "priority": "Medium",
                    "status": "Open"
                },
                "management_response": "",
                "status": "Open"
            })
            request_counter += 1

        control_coverage = item_score.get("control_atlas_mapping", {}).get("control_coverage_score", 100)
        if control_coverage < 50:
            findings.append({
                "finding_id": f"SEN-{request_counter:03d}",
                "title": "Control Atlas Coverage Gap",
                "severity": "Medium",
                "severity_rationale": f"Mapped control coverage is {control_coverage}/100 for the detected domain.",
                "risk_domain": item_score["domain"],
                "affected_item": item.title,
                "dimension": "Control Atlas Coverage",
                "issue": "The evidence does not sufficiently cover expected control atlas requirements.",
                "evidence_gap": "Missing control evidence: " + ", ".join(item_score["control_atlas_mapping"]["missing_evidence_summary"]),
                "examiner_question": "Which control objective is this evidence intended to support, and what expected evidence remains missing?",
                "remediation": "Collect missing control evidence or document why the evidence requirement is not applicable.",
                "framework_relevance": [m["framework"] for m in framework_mappings_for(item_score["domain"])],
                "framework_mappings": framework_mappings_for(item_score["domain"]),
                "control_atlas_ids": [c["control_id"] for c in item_score["control_atlas_mapping"].get("mapped_controls", [])],
                "evidence_request": {
                    "request_id": f"REQ-{request_counter:03d}",
                    "evidence_needed": "Provide missing control atlas evidence: " + ", ".join(item_score["control_atlas_mapping"]["missing_evidence_summary"][:10]),
                    "preferred_artifacts": item_score["control_atlas_mapping"]["missing_evidence_summary"][:10],
                    "owner": item.owner or "Evidence Owner",
                    "priority": "Medium",
                    "status": "Open"
                },
                "management_response": "",
                "status": "Open"
            })
            request_counter += 1

    if not findings:
        domain = item_scores[0]["domain"] if item_scores else "General Evidence Defensibility"
        findings.append(build_finding(
            EvidenceItem(title="Overall Evidence Package", content="General positive review", owner="Evidence Owner"),
            {"domain": domain, "control_atlas_mapping": map_control_atlas(domain, "general positive review")},
            {"key": "general", "label": "General Review", "score": 85, "rating": "Strong", "positive_indicators": ["general"], "negative_indicators": []},
            1
        ))

    overall_score = round(sum(i["score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    intake_score = round(sum(i["intake_gap_analysis"]["intake_coverage_score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    metadata_score = round(sum(i["artifact_profile"]["metadata_completeness_score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    control_coverage_score = round(sum(i["control_atlas_mapping"]["control_coverage_score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    rating = "Strong" if overall_score >= 85 else "Moderate" if overall_score >= 70 else "Weak" if overall_score >= 50 else "Critical Attention Required"

    severity_distribution, domain_counts, framework_counts, control_counts = {}, {}, {}, {}
    for finding in findings:
        severity_distribution[finding["severity"]] = severity_distribution.get(finding["severity"], 0) + 1
        domain_counts[finding["risk_domain"]] = domain_counts.get(finding["risk_domain"], 0) + 1
        for fw in finding["framework_relevance"]:
            framework_counts[fw] = framework_counts.get(fw, 0) + 1
        for cid in finding.get("control_atlas_ids", []):
            control_counts[cid] = control_counts.get(cid, 0) + 1

    evidence_requests = [f["evidence_request"] for f in findings]
    executive_summary = (
        f"Sentinel reviewed {len(payload.items)} evidence item(s). The package is rated '{rating}' "
        f"with an evidence defensibility score of {overall_score}/100, intake coverage score of {intake_score}/100, "
        f"metadata completeness score of {metadata_score}/100, and control atlas coverage score of {control_coverage_score}/100. "
        f"{len(findings)} finding(s) and {len(evidence_requests)} evidence request(s) were generated."
    )

    return {
        "product": "Sentinel Evidence Defensibility Workbench",
        "company": "Eye On Bits Pvt Ltd",
        "version": "10.1.1",
        "review_timestamp": datetime.utcnow().isoformat(),
        "organization": payload.organization,
        "industry": payload.industry,
        "evidence_type": payload.evidence_type,
        "review_objective": payload.review_objective,
        "evidence_defensibility_score": overall_score,
        "intake_coverage_score": intake_score,
        "metadata_completeness_score": metadata_score,
        "control_atlas_coverage_score": control_coverage_score,
        "overall_rating": rating,
        "total_findings": len(findings),
        "high_risk_findings": len([f for f in findings if f["severity"] in ["Critical", "High"]]),
        "severity_distribution": severity_distribution,
        "top_risk_domains": sorted([{"domain": k, "count": v} for k, v in domain_counts.items()], key=lambda x: x["count"], reverse=True),
        "framework_coverage": sorted([{"framework": k, "count": v} for k, v in framework_counts.items()], key=lambda x: x["count"], reverse=True),
        "control_atlas_coverage": sorted([{"control_id": k, "finding_count": v} for k, v in control_counts.items()], key=lambda x: x["finding_count"], reverse=True),
        "item_scorecards": item_scores,
        "findings": findings,
        "evidence_requests": evidence_requests,
        "recommended_next_steps": [
            "Address missing metadata first: owner, source system, reporting period, evidence date, and control reference.",
            "Review Control Atlas mappings and collect missing expected control evidence.",
            "Use the challenge question bank to conduct 2LOD-style or audit-style follow-up.",
            "Update the remediation register with owner, target date, management response, and closure evidence.",
            "Re-run Sentinel after remediation evidence is collected."
        ],
        "executive_summary": executive_summary
    }

def save_review(payload: AnalyzeRequest, result: Dict[str, Any]) -> Dict[str, Any]:
    ensure_db()
    review_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    register = build_register(result)
    result_with_id = dict(result)
    result_with_id["review_id"] = review_id
    result_with_id["remediation_register"] = register
    with db() as conn:
        conn.execute("""
            INSERT INTO reviews (
                id, created_at, updated_at, organization, industry, evidence_type, review_objective,
                overall_rating, evidence_defensibility_score, intake_coverage_score, metadata_completeness_score,
                total_findings, payload_json, result_json, register_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            review_id, now, now, payload.organization, payload.industry, payload.evidence_type, payload.review_objective,
            result["overall_rating"], result["evidence_defensibility_score"], result["intake_coverage_score"],
            result["metadata_completeness_score"], result["total_findings"], json.dumps(payload.model_dump()),
            json.dumps(result_with_id), json.dumps(register)
        ))
        conn.commit()
    return result_with_id

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Sentinel Evidence Defensibility Workbench", "version": "10.1.1", "database": str(DB_PATH), "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/control-atlas")
def control_atlas():
    return CONTROL_ATLAS

@app.get("/api/framework-library")
def framework_library():
    return FRAMEWORK_LIBRARY

@app.get("/api/scoring-dimensions")
def scoring_dimensions():
    return DIMENSIONS

@app.get("/api/intake-requirements")
def intake_requirements():
    return INTAKE_REQUIREMENTS

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    return build_analysis(payload)

@app.post("/api/reviews/analyze-save")
def analyze_and_save(payload: AnalyzeRequest):
    return save_review(payload, build_analysis(payload))

@app.get("/api/reviews")
def list_reviews():
    ensure_db()
    with db() as conn:
        rows = conn.execute("""
            SELECT id, created_at, updated_at, organization, industry, evidence_type, overall_rating,
                   evidence_defensibility_score, intake_coverage_score, metadata_completeness_score, total_findings
            FROM reviews ORDER BY created_at DESC
        """).fetchall()
    return [dict(row) for row in rows]

@app.get("/api/reviews/{review_id}")
def get_review(review_id: str):
    ensure_db()
    with db() as conn:
        row = conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Review not found")
    result = json.loads(row["result_json"])
    result["remediation_register"] = json.loads(row["register_json"])
    return result

@app.put("/api/reviews/{review_id}/register")
def replace_register(review_id: str, update: RegisterUpdate):
    ensure_db()
    now = datetime.utcnow().isoformat()
    with db() as conn:
        row = conn.execute("SELECT result_json FROM reviews WHERE id = ?", (review_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Review not found")
        result = json.loads(row["result_json"])
        result["remediation_register"] = update.rows
        conn.execute("UPDATE reviews SET updated_at = ?, result_json = ?, register_json = ? WHERE id = ?", (now, json.dumps(result), json.dumps(update.rows), review_id))
        conn.commit()
    return {"status": "saved", "review_id": review_id, "updated_at": now, "register_rows": len(update.rows)}

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: str):
    ensure_db()
    with db() as conn:
        cur = conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"status": "deleted", "review_id": review_id}

def _portfolio_snapshot_from_reviews(rows: List[sqlite3.Row]) -> Dict[str, Any]:
    reviews = [dict(row) for row in rows]
    total_reviews = len(reviews)
    avg_defensibility = round(sum((r.get("evidence_defensibility_score") or 0) for r in reviews) / total_reviews) if total_reviews else 0
    avg_intake = round(sum((r.get("intake_coverage_score") or 0) for r in reviews) / total_reviews) if total_reviews else 0
    avg_metadata = round(sum((r.get("metadata_completeness_score") or 0) for r in reviews) / total_reviews) if total_reviews else 0
    total_findings = sum((r.get("total_findings") or 0) for r in reviews)
    rating_distribution, evidence_type_distribution, domain_counts, status_counts, severity_counts, control_counts = {}, {}, {}, {}, {}, {}
    open_register_items, in_progress_register_items, closed_register_items, high_or_critical_items = 0, 0, 0, 0

    with db() as conn:
        full_rows = conn.execute("SELECT register_json, result_json FROM reviews").fetchall()

    for r in reviews:
        rating_distribution[r.get("overall_rating") or "Unknown"] = rating_distribution.get(r.get("overall_rating") or "Unknown", 0) + 1
        evidence_type_distribution[r.get("evidence_type") or "Unknown"] = evidence_type_distribution.get(r.get("evidence_type") or "Unknown", 0) + 1

    for row in full_rows:
        register = json.loads(row["register_json"])
        result = json.loads(row["result_json"])
        for finding in result.get("findings", []):
            sev = finding.get("severity", "Unknown")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            if sev in ["High", "Critical"]:
                high_or_critical_items += 1
            domain = finding.get("risk_domain", "Unknown")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
            for cid in finding.get("control_atlas_ids", []):
                control_counts[cid] = control_counts.get(cid, 0) + 1
        for item in register:
            status = item.get("status", "Open")
            status_counts[status] = status_counts.get(status, 0) + 1
            if status == "Closed":
                closed_register_items += 1
            elif status == "In Progress":
                in_progress_register_items += 1
            else:
                open_register_items += 1

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "total_reviews": total_reviews,
        "average_defensibility_score": avg_defensibility,
        "average_intake_score": avg_intake,
        "average_metadata_score": avg_metadata,
        "total_findings": total_findings,
        "high_or_critical_findings": high_or_critical_items,
        "open_register_items": open_register_items,
        "in_progress_register_items": in_progress_register_items,
        "closed_register_items": closed_register_items,
        "rating_distribution": rating_distribution,
        "evidence_type_distribution": evidence_type_distribution,
        "severity_distribution": severity_counts,
        "risk_domain_distribution": domain_counts,
        "register_status_distribution": status_counts,
        "control_atlas_distribution": control_counts,
        "reviews": reviews
    }

@app.get("/api/portfolio")
def portfolio_dashboard():
    ensure_db()
    with db() as conn:
        rows = conn.execute("""
            SELECT id, created_at, updated_at, organization, industry, evidence_type, overall_rating,
                   evidence_defensibility_score, intake_coverage_score, metadata_completeness_score, total_findings
            FROM reviews ORDER BY created_at DESC
        """).fetchall()
    return _portfolio_snapshot_from_reviews(rows)

@app.post("/api/demo/seed")
def seed_demo_reviews():
    examples = [
        {
            "organization": "Sample Tier-1 Bank",
            "industry": "BFSI / Regulated Banking",
            "evidence_type": "IT Metrics Defensibility Review",
            "review_objective": "Assess denominator consistency, source lineage, calculation logic, and committee reporting tie-out.",
            "items": [{"title": "Q4 Phishing Metric Evidence", "content": "The ITSC deck reported 150 delivered emails. KnowBe4 source export shows denominator changed to 152. Screenshot-only evidence was retained. No reviewer approval or reconciliation is attached.", "source_system": "KnowBe4 / ITSC Deck", "owner": "IT GRC", "reporting_period": "Q4", "artifact_type": "Metric Evidence"}]
        },
        {
            "organization": "Sample Financial Institution",
            "industry": "BFSI / Vendor Risk",
            "evidence_type": "Vendor and Privacy Evidence Review",
            "review_objective": "Assess SOC 2 reliance, CUEC analysis, data-flow evidence, retention, and customer information handling.",
            "items": [{"title": "Vendor SOC 2 Evidence", "content": "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, bridge letter, subservice organization review, DPA, or CUEC analysis.", "source_system": "Vendor Portal", "owner": "TPRM", "reporting_period": "Annual Review", "artifact_type": "SOC 2 / Vendor Evidence"}]
        },
        {
            "organization": "Sample Enterprise Technology Group",
            "industry": "Technology / AI Governance",
            "evidence_type": "SDLC and AI Governance Review",
            "review_objective": "Assess release governance, AI approval, security gates, monitoring, and production readiness evidence.",
            "items": [{"title": "AI-Enabled Release Evidence", "content": "Release notes mention AI assistant functionality and production rollout. No AI inventory entry, risk tier, approval record, security gate, change record, monitoring plan, or incident escalation logic.", "source_system": "DevOps Release Tracker", "owner": "Application Owner", "reporting_period": "Release 2026.05", "artifact_type": "AI Release Evidence"}]
        }
    ]
    saved = []
    for example in examples:
        payload = AnalyzeRequest(**example)
        saved.append(save_review(payload, build_analysis(payload)))
    return {"status": "seeded", "reviews_created": len(saved), "review_ids": [x["review_id"] for x in saved]}

def render_html_report(result: Dict[str, Any]) -> str:
    score_rows = ""
    for item in result["item_scorecards"]:
        control_rows = ""
        for control in item.get("control_atlas_mapping", {}).get("mapped_controls", []):
            control_rows += f"<tr><td>{html.escape(control['control_id'])}</td><td>{html.escape(control['control_theme'])}</td><td>{control['control_coverage_score']}/100</td><td>{html.escape(', '.join(control['missing_evidence']))}</td></tr>"
        score_rows += f"""
        <div class='finding'>
          <h3>{html.escape(item['item_title'])}</h3>
          <p><b>Domain:</b> {html.escape(item['domain'])} | <b>Score:</b> {item['score']}/100 | <b>Control Atlas:</b> {item['control_atlas_mapping']['control_coverage_score']}/100</p>
          <table><tr><th>Control ID</th><th>Theme</th><th>Coverage</th><th>Missing Evidence</th></tr>{control_rows}</table>
        </div>
        """
    register_rows = ""
    for row in result.get("remediation_register", []):
        register_rows += f"<tr><td>{html.escape(str(row.get('finding_id','')))}</td><td>{html.escape(str(row.get('severity','')))}</td><td>{html.escape(str(row.get('control_atlas_ids','')))}</td><td>{html.escape(str(row.get('owner','')))}</td><td>{html.escape(str(row.get('status','')))}</td><td>{html.escape(str(row.get('management_response','')))}</td></tr>"
    finding_blocks = ""
    for f in result["findings"]:
        finding_blocks += f"""
        <div class='finding'>
          <h3>{html.escape(f['finding_id'])} — {html.escape(f['title'])}</h3>
          <p><b>Severity:</b> {html.escape(f['severity'])} | <b>Risk domain:</b> {html.escape(f['risk_domain'])} | <b>Control Atlas:</b> {html.escape(', '.join(f.get('control_atlas_ids', [])))}</p>
          <p><b>Issue:</b> {html.escape(f['issue'])}</p>
          <p><b>Evidence gap:</b> {html.escape(f['evidence_gap'])}</p>
          <p><b>Examiner question:</b> {html.escape(f['examiner_question'])}</p>
        </div>
        """
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Evidence Defensibility Report</title>
<style>
body {{ font-family: Arial, sans-serif; background:#f6f8fb; color:#111827; margin:0; padding:32px; }}
.report {{ max-width:1240px; margin:auto; background:white; border-radius:18px; padding:36px; box-shadow:0 20px 60px rgba(15,23,42,.12); }}
.eyebrow {{ color:#1d4ed8; text-transform:uppercase; letter-spacing:.18em; font-size:12px; font-weight:800; }}
h1 {{ font-size:38px; margin:8px 0; }}
.cards {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin:24px 0; }}
.card {{ background:#f9fafb; border:1px solid #e5e7eb; border-radius:14px; padding:16px; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:22px; margin-top:6px; }}
.summary {{ border-left:5px solid #1d4ed8; background:#eff6ff; padding:16px; border-radius:12px; margin:18px 0; }}
.finding {{ border:1px solid #e5e7eb; border-radius:14px; padding:18px; margin:16px 0; }}
table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }}
th,td {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; vertical-align:top; }}
</style>
</head>
<body>
<div class='report'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Evidence Defensibility and Control Atlas Report</h1>
<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(result['organization'])}</strong></div>
<div class='card'><span>Defensibility</span><strong>{result['evidence_defensibility_score']}/100</strong></div>
<div class='card'><span>Intake</span><strong>{result['intake_coverage_score']}/100</strong></div>
<div class='card'><span>Metadata</span><strong>{result['metadata_completeness_score']}/100</strong></div>
<div class='card'><span>Control Atlas</span><strong>{result['control_atlas_coverage_score']}/100</strong></div>
</div>
<div class='summary'>{html.escape(result['executive_summary'])}</div>
<h2>Remediation Register</h2><table><tr><th>Finding</th><th>Severity</th><th>Control Atlas IDs</th><th>Owner</th><th>Status</th><th>Management Response</th></tr>{register_rows}</table>
<h2>Control Atlas Scorecards</h2>{score_rows}
<h2>Findings</h2>{finding_blocks}
</div>
</body>
</html>"""

@app.post("/api/report-html", response_class=HTMLResponse)
def report_html(payload: AnalyzeRequest):
    result = build_analysis(payload)
    result["remediation_register"] = build_register(result)
    return render_html_report(result)

@app.get("/api/reviews/{review_id}/report-html", response_class=HTMLResponse)
def saved_report_html(review_id: str):
    return render_html_report(get_review(review_id))

@app.get("/api/portfolio/report-html", response_class=HTMLResponse)
def portfolio_report_html():
    snapshot = portfolio_dashboard()
    control_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot["control_atlas_distribution"].items(), key=lambda x: x[1], reverse=True))
    domain_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot["risk_domain_distribution"].items(), key=lambda x: x[1], reverse=True))
    severity_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot["severity_distribution"].items(), key=lambda x: x[1], reverse=True))
    review_rows = "".join(f"<tr><td>{html.escape(str(r.get('organization','')))}</td><td>{html.escape(str(r.get('evidence_type','')))}</td><td>{html.escape(str(r.get('overall_rating','')))}</td><td>{r.get('evidence_defensibility_score','')}/100</td><td>{r.get('total_findings','')}</td></tr>" for r in snapshot["reviews"])
    return f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>Sentinel Portfolio Control Atlas Report</title>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#111827;margin:0;padding:32px}}
.report{{max-width:1280px;margin:auto;background:white;border-radius:20px;padding:36px;box-shadow:0 20px 60px rgba(15,23,42,.12)}}
.cards{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:24px 0}}
.card{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:14px;padding:16px}}
.card span{{display:block;color:#6b7280;font-size:12px;text-transform:uppercase}}.card strong{{display:block;font-size:23px;margin-top:6px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}.panel{{border:1px solid #e5e7eb;border-radius:16px;padding:18px;margin:16px 0}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}}th,td{{border-bottom:1px solid #e5e7eb;padding:10px;text-align:left;vertical-align:top}}
</style></head><body><div class='report'>
<h1>Sentinel Portfolio Control Atlas Report</h1>
<div class='cards'><div class='card'><span>Total Reviews</span><strong>{snapshot['total_reviews']}</strong></div><div class='card'><span>Avg Defensibility</span><strong>{snapshot['average_defensibility_score']}/100</strong></div><div class='card'><span>Total Findings</span><strong>{snapshot['total_findings']}</strong></div><div class='card'><span>High/Critical</span><strong>{snapshot['high_or_critical_findings']}</strong></div><div class='card'><span>Open Items</span><strong>{snapshot['open_register_items']}</strong></div></div>
<div class='grid'><div class='panel'><h2>Control Atlas</h2><table><tr><th>Control</th><th>Findings</th></tr>{control_rows}</table></div><div class='panel'><h2>Domains</h2><table><tr><th>Domain</th><th>Count</th></tr>{domain_rows}</table></div><div class='panel'><h2>Severity</h2><table><tr><th>Severity</th><th>Count</th></tr>{severity_rows}</table></div></div>
<h2>Saved Reviews</h2><table><tr><th>Organization</th><th>Evidence Type</th><th>Rating</th><th>Score</th><th>Findings</th></tr>{review_rows}</table>
</div></body></html>"""


def build_board_pack_from_result(result: Dict[str, Any]) -> Dict[str, Any]:
    findings = result.get("findings", [])
    register = result.get("remediation_register", [])
    item_scorecards = result.get("item_scorecards", [])

    high_findings = [f for f in findings if f.get("severity") in ["High", "Critical"]]
    medium_findings = [f for f in findings if f.get("severity") == "Medium"]

    open_items = [r for r in register if r.get("status", "Open") not in ["Closed"]]
    closed_items = [r for r in register if r.get("status") == "Closed"]

    domains: Dict[str, int] = {}
    controls: Dict[str, int] = {}
    missing_evidence: Dict[str, int] = {}
    challenge_questions: List[str] = []

    for item in item_scorecards:
        domain = item.get("domain", "Unknown")
        domains[domain] = domains.get(domain, 0) + 1

        atlas = item.get("control_atlas_mapping", {})
        for control in atlas.get("mapped_controls", []):
            cid = control.get("control_id", "Unknown")
            controls[cid] = controls.get(cid, 0) + 1

            for evidence in control.get("missing_evidence", []):
                missing_evidence[evidence] = missing_evidence.get(evidence, 0) + 1

            for question in control.get("challenge_questions", []):
                if question not in challenge_questions:
                    challenge_questions.append(question)

    top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    top_controls = sorted(controls.items(), key=lambda x: x[1], reverse=True)
    top_missing = sorted(missing_evidence.items(), key=lambda x: x[1], reverse=True)

    business_narrative = (
        f"The review of {result.get('organization')} produced an overall evidence defensibility rating of "
        f"{result.get('overall_rating')} with a defensibility score of {result.get('evidence_defensibility_score')}/100. "
        f"The review identified {result.get('total_findings')} finding(s), including {len(high_findings)} high or critical item(s). "
        f"The control atlas coverage score is {result.get('control_atlas_coverage_score', 'N/A')}/100, indicating the extent to which submitted evidence aligns to expected control objectives and supporting artifacts."
    )

    board_message = (
        "The primary concern is not merely whether evidence exists, but whether evidence is reliable enough for management, audit, "
        "or examiner reliance. The immediate management focus should be on source lineage, ownership, review approval, missing control evidence, "
        "and closure artifacts for open remediation items."
    )

    action_plan = [
        {
            "phase": "0-7 days",
            "focus": "Stabilize evidence ownership and source lineage",
            "actions": [
                "Assign accountable owner for each open finding.",
                "Confirm source system and reporting period for each evidence item.",
                "Collect missing source exports, approval evidence, and reconciliation support for high-priority gaps."
            ]
        },
        {
            "phase": "8-21 days",
            "focus": "Remediate control evidence gaps",
            "actions": [
                "Use the Control Atlas missing evidence list to collect expected artifacts.",
                "Document management response and remediation commitment for each finding.",
                "Validate whether risk acceptance is required for evidence that cannot be produced."
            ]
        },
        {
            "phase": "22-30 days",
            "focus": "Prepare closure and governance reporting",
            "actions": [
                "Attach closure evidence and reviewer validation notes.",
                "Export remediation register for management review.",
                "Re-run Sentinel to confirm improved defensibility and control coverage scores."
            ]
        }
    ]

    board_questions = [
        "Which evidence gaps create the highest audit or examiner reliance risk?",
        "Which findings lack a named owner, target date, or closure path?",
        "Which missing artifacts prevent management from validating the control claim?",
        "Are any open issues suitable for formal risk acceptance rather than remediation?",
        "What improvement should be expected in the defensibility score after remediation evidence is provided?"
    ]

    management_prompts = [
        "Provide a source-of-record artifact for the reported value or control claim.",
        "Explain whether the missing evidence is unavailable, not applicable, retained elsewhere, or pending collection.",
        "Identify the accountable owner, target date, and expected closure evidence.",
        "Document whether a temporary risk acceptance is needed until evidence is produced.",
        "Confirm how management will prevent recurrence in the next reporting cycle."
    ]

    return {
        "product": "Sentinel Board Pack Studio",
        "version": "10.1.1",
        "generated_at": datetime.utcnow().isoformat(),
        "review_id": result.get("review_id"),
        "organization": result.get("organization"),
        "evidence_type": result.get("evidence_type"),
        "overall_rating": result.get("overall_rating"),
        "evidence_defensibility_score": result.get("evidence_defensibility_score"),
        "control_atlas_coverage_score": result.get("control_atlas_coverage_score"),
        "intake_coverage_score": result.get("intake_coverage_score"),
        "metadata_completeness_score": result.get("metadata_completeness_score"),
        "total_findings": result.get("total_findings"),
        "high_or_critical_findings": len(high_findings),
        "open_register_items": len(open_items),
        "closed_register_items": len(closed_items),
        "business_narrative": business_narrative,
        "board_message": board_message,
        "top_domains": [{"domain": k, "count": v} for k, v in top_domains],
        "top_control_atlas_ids": [{"control_id": k, "count": v} for k, v in top_controls],
        "top_missing_evidence": [{"artifact": k, "count": v} for k, v in top_missing],
        "board_questions": board_questions,
        "control_challenge_questions": challenge_questions[:12],
        "management_prompts": management_prompts,
        "thirty_day_action_plan": action_plan,
        "high_priority_findings": [
            {
                "finding_id": f.get("finding_id"),
                "severity": f.get("severity"),
                "risk_domain": f.get("risk_domain"),
                "control_atlas_ids": f.get("control_atlas_ids", []),
                "issue": f.get("issue"),
                "evidence_gap": f.get("evidence_gap"),
                "examiner_question": f.get("examiner_question"),
                "remediation": f.get("remediation")
            }
            for f in high_findings[:10]
        ],
        "open_remediation_items": open_items[:25]
    }

def render_board_pack_html(pack: Dict[str, Any]) -> str:
    domain_rows = "".join(
        f"<tr><td>{html.escape(str(x.get('domain','')))}</td><td>{x.get('count','')}</td></tr>"
        for x in pack.get("top_domains", [])
    )

    control_rows = "".join(
        f"<tr><td>{html.escape(str(x.get('control_id','')))}</td><td>{x.get('count','')}</td></tr>"
        for x in pack.get("top_control_atlas_ids", [])
    )

    missing_rows = "".join(
        f"<tr><td>{html.escape(str(x.get('artifact','')))}</td><td>{x.get('count','')}</td></tr>"
        for x in pack.get("top_missing_evidence", [])
    )

    question_items = "".join(f"<li>{html.escape(q)}</li>" for q in pack.get("board_questions", []))
    challenge_items = "".join(f"<li>{html.escape(q)}</li>" for q in pack.get("control_challenge_questions", []))
    prompt_items = "".join(f"<li>{html.escape(q)}</li>" for q in pack.get("management_prompts", []))

    plan_blocks = ""
    for phase in pack.get("thirty_day_action_plan", []):
        actions = "".join(f"<li>{html.escape(a)}</li>" for a in phase.get("actions", []))
        plan_blocks += f"""
        <div class='phase'>
          <h3>{html.escape(phase.get('phase',''))} — {html.escape(phase.get('focus',''))}</h3>
          <ul>{actions}</ul>
        </div>
        """

    finding_blocks = ""
    for finding in pack.get("high_priority_findings", []):
        finding_blocks += f"""
        <div class='finding'>
          <h3>{html.escape(str(finding.get('finding_id','')))} — {html.escape(str(finding.get('severity','')))}</h3>
          <p><b>Risk Domain:</b> {html.escape(str(finding.get('risk_domain','')))}</p>
          <p><b>Control Atlas:</b> {html.escape(', '.join(finding.get('control_atlas_ids', [])))}</p>
          <p><b>Issue:</b> {html.escape(str(finding.get('issue','')))}</p>
          <p><b>Evidence Gap:</b> {html.escape(str(finding.get('evidence_gap','')))}</p>
          <p><b>Examiner Question:</b> {html.escape(str(finding.get('examiner_question','')))}</p>
          <p><b>Remediation:</b> {html.escape(str(finding.get('remediation','')))}</p>
        </div>
        """

    open_rows = ""
    for item in pack.get("open_remediation_items", []):
        open_rows += f"""
        <tr>
          <td>{html.escape(str(item.get('finding_id','')))}</td>
          <td>{html.escape(str(item.get('severity','')))}</td>
          <td>{html.escape(str(item.get('owner','')))}</td>
          <td>{html.escape(str(item.get('target_date','')))}</td>
          <td>{html.escape(str(item.get('status','')))}</td>
          <td>{html.escape(str(item.get('evidence_needed','')))}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Board Pack Studio</title>
<style>
body {{ font-family: Arial, sans-serif; background:#f5f7fb; color:#111827; margin:0; padding:32px; }}
.pack {{ max-width:1280px; margin:auto; background:white; border-radius:22px; padding:38px; box-shadow:0 20px 70px rgba(15,23,42,.13); }}
.eyebrow {{ color:#1d4ed8; text-transform:uppercase; letter-spacing:.18em; font-size:12px; font-weight:800; }}
h1 {{ margin:8px 0 8px; font-size:40px; letter-spacing:-.04em; }}
.sub {{ color:#4b5563; }}
.cards {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin:24px 0; }}
.card {{ background:#f9fafb; border:1px solid #e5e7eb; border-radius:14px; padding:16px; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:23px; margin-top:6px; }}
.summary {{ border-left:5px solid #1d4ed8; background:#eff6ff; padding:16px; border-radius:12px; margin:18px 0; line-height:1.5; }}
.grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin:18px 0; }}
.panel, .phase, .finding {{ border:1px solid #e5e7eb; border-radius:16px; padding:18px; margin:16px 0; background:#ffffff; }}
table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }}
th,td {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; vertical-align:top; }}
li {{ margin:7px 0; }}
.footer {{ color:#6b7280; font-size:12px; margin-top:24px; }}
@media print {{ body {{ background:white; padding:0; }} .pack {{ box-shadow:none; }} }}
</style>
</head>
<body>
<div class='pack'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Board Pack Studio</h1>
<p class='sub'>Board-ready evidence defensibility narrative, risk themes, missing evidence, challenge questions, and 30-day action plan.</p>

<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(str(pack.get('organization','')))}</strong></div>
<div class='card'><span>Rating</span><strong>{html.escape(str(pack.get('overall_rating','')))}</strong></div>
<div class='card'><span>Defensibility</span><strong>{pack.get('evidence_defensibility_score','')}/100</strong></div>
<div class='card'><span>Control Atlas</span><strong>{pack.get('control_atlas_coverage_score','')}/100</strong></div>
<div class='card'><span>Open Items</span><strong>{pack.get('open_register_items','')}</strong></div>
</div>

<div class='summary'><b>Executive Narrative:</b> {html.escape(pack.get('business_narrative',''))}</div>
<div class='summary'><b>Board Message:</b> {html.escape(pack.get('board_message',''))}</div>

<div class='grid'>
<div class='panel'><h2>Top Risk Domains</h2><table><tr><th>Domain</th><th>Count</th></tr>{domain_rows}</table></div>
<div class='panel'><h2>Control Atlas Concentration</h2><table><tr><th>Control ID</th><th>Count</th></tr>{control_rows}</table></div>
<div class='panel'><h2>Missing Evidence</h2><table><tr><th>Artifact</th><th>Count</th></tr>{missing_rows}</table></div>
</div>

<div class='panel'><h2>Board Questions</h2><ol>{question_items}</ol></div>
<div class='panel'><h2>Control Challenge Questions</h2><ol>{challenge_items}</ol></div>
<div class='panel'><h2>Management Response Prompts</h2><ol>{prompt_items}</ol></div>

<h2>30-Day Action Plan</h2>
{plan_blocks}

<h2>High-Priority Findings</h2>
{finding_blocks}

<h2>Open Remediation Items</h2>
<table><tr><th>Finding</th><th>Severity</th><th>Owner</th><th>Target Date</th><th>Status</th><th>Evidence Needed</th></tr>{open_rows}</table>

<div class='footer'>Generated by Sentinel Evidence Defensibility Workbench v6.0. This output supports management and board-style evidence assurance discussion.</div>
</div>
</body>
</html>"""

@app.get("/api/reviews/{review_id}/board-pack")
def saved_review_board_pack(review_id: str):
    result = get_review(review_id)
    return build_board_pack_from_result(result)

@app.get("/api/reviews/{review_id}/board-pack-html", response_class=HTMLResponse)
def saved_review_board_pack_html(review_id: str):
    result = get_review(review_id)
    return render_board_pack_html(build_board_pack_from_result(result))

@app.get("/api/portfolio/board-pack-html", response_class=HTMLResponse)
def portfolio_board_pack_html():
    snapshot = portfolio_dashboard()
    domain_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot.get('risk_domain_distribution', {}).items(), key=lambda x: x[1], reverse=True))
    control_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot.get('control_atlas_distribution', {}).items(), key=lambda x: x[1], reverse=True))
    review_rows = "".join(f"<tr><td>{html.escape(str(r.get('organization','')))}</td><td>{html.escape(str(r.get('evidence_type','')))}</td><td>{html.escape(str(r.get('overall_rating','')))}</td><td>{r.get('evidence_defensibility_score','')}/100</td><td>{r.get('total_findings','')}</td></tr>" for r in snapshot.get("reviews", []))

    narrative = (
        f"The portfolio contains {snapshot.get('total_reviews')} saved review(s), with an average defensibility score of "
        f"{snapshot.get('average_defensibility_score')}/100 and {snapshot.get('total_findings')} total finding(s). "
        f"There are {snapshot.get('open_register_items')} open remediation item(s), including "
        f"{snapshot.get('high_or_critical_findings')} high or critical finding(s)."
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Portfolio Board Pack</title>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#111827;margin:0;padding:32px}}
.pack{{max-width:1280px;margin:auto;background:white;border-radius:22px;padding:38px;box-shadow:0 20px 70px rgba(15,23,42,.13)}}
.eyebrow{{color:#1d4ed8;text-transform:uppercase;letter-spacing:.18em;font-size:12px;font-weight:800}}
h1{{margin:8px 0;font-size:40px}}.summary{{border-left:5px solid #1d4ed8;background:#eff6ff;padding:16px;border-radius:12px;margin:18px 0;line-height:1.5}}
.cards{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:24px 0}}.card{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:14px;padding:16px}}
.card span{{display:block;color:#6b7280;font-size:12px;text-transform:uppercase}}.card strong{{display:block;font-size:23px;margin-top:6px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.panel{{border:1px solid #e5e7eb;border-radius:16px;padding:18px;margin:16px 0}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}}th,td{{border-bottom:1px solid #e5e7eb;padding:10px;text-align:left;vertical-align:top}}
</style>
</head>
<body>
<div class='pack'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Portfolio Board Pack</h1>
<div class='cards'>
<div class='card'><span>Total Reviews</span><strong>{snapshot.get('total_reviews')}</strong></div>
<div class='card'><span>Avg Defensibility</span><strong>{snapshot.get('average_defensibility_score')}/100</strong></div>
<div class='card'><span>Total Findings</span><strong>{snapshot.get('total_findings')}</strong></div>
<div class='card'><span>High/Critical</span><strong>{snapshot.get('high_or_critical_findings')}</strong></div>
<div class='card'><span>Open Items</span><strong>{snapshot.get('open_register_items')}</strong></div>
</div>
<div class='summary'>{html.escape(narrative)}</div>
<div class='grid'><div class='panel'><h2>Risk Domains</h2><table><tr><th>Domain</th><th>Count</th></tr>{domain_rows}</table></div><div class='panel'><h2>Control Atlas Concentration</h2><table><tr><th>Control</th><th>Count</th></tr>{control_rows}</table></div></div>
<h2>Saved Reviews</h2><table><tr><th>Organization</th><th>Evidence Type</th><th>Rating</th><th>Score</th><th>Findings</th></tr>{review_rows}</table>
</div>
</body>
</html>"""


def _closure_readiness_score(row: Dict[str, Any]) -> Dict[str, Any]:
    checks = [
        ("owner", "Owner assigned"),
        ("target_date", "Target date assigned"),
        ("management_response", "Management response captured"),
        ("closure_evidence", "Closure evidence referenced"),
        ("validation_notes", "Reviewer validation notes captured")
    ]

    completed = []
    missing = []

    for field, label in checks:
        if str(row.get(field, "")).strip():
            completed.append(label)
        else:
            missing.append(label)

    if row.get("status") == "Closed":
        completed.append("Status marked closed")
    else:
        missing.append("Status not closed")

    score = round((len(completed) / (len(completed) + len(missing))) * 100) if (completed or missing) else 0
    rating = "Ready for Closure Review" if score >= 85 else "Partially Ready" if score >= 55 else "Not Ready"

    return {
        "score": score,
        "rating": rating,
        "completed": completed,
        "missing": missing
    }

def build_evidence_request_studio_pack(result: Dict[str, Any]) -> Dict[str, Any]:
    findings = result.get("findings", [])
    register = result.get("remediation_register", [])

    register_by_finding = {row.get("finding_id"): row for row in register}
    request_rows = []
    closure_rows = []
    owner_counts: Dict[str, int] = {}
    priority_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}

    for finding in findings:
        request = finding.get("evidence_request", {})
        fid = finding.get("finding_id")
        reg = register_by_finding.get(fid, {})
        owner = reg.get("owner") or request.get("owner") or "Evidence Owner"
        priority = request.get("priority") or finding.get("severity") or "Medium"
        status = reg.get("status") or request.get("status") or "Open"

        owner_counts[owner] = owner_counts.get(owner, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

        artifacts = request.get("preferred_artifacts", [])
        if isinstance(artifacts, str):
            artifacts = [artifacts]

        request_message = (
            f"Please provide evidence for {fid} ({finding.get('title')}). "
            f"The current gap relates to {finding.get('risk_domain')} and mapped control(s): "
            f"{', '.join(finding.get('control_atlas_ids', [])) or 'Not mapped'}. "
            f"Evidence needed: {request.get('evidence_needed', finding.get('evidence_gap'))}. "
            f"Preferred artifacts: {', '.join(artifacts) if artifacts else 'supporting evidence package'}. "
            f"Please also provide owner confirmation, evidence date, source system, and reviewer approval where applicable."
        )

        validation_test = (
            f"Reviewer should confirm that the evidence directly supports the control claim, ties to the source system, "
            f"covers the reporting period, and resolves the finding without relying only on verbal confirmation."
        )

        request_rows.append({
            "request_id": request.get("request_id"),
            "finding_id": fid,
            "priority": priority,
            "owner": owner,
            "status": status,
            "target_date": reg.get("target_date", ""),
            "risk_domain": finding.get("risk_domain"),
            "control_atlas_ids": finding.get("control_atlas_ids", []),
            "evidence_needed": request.get("evidence_needed", finding.get("evidence_gap")),
            "preferred_artifacts": artifacts,
            "request_message": request_message,
            "validation_test": validation_test,
            "closure_criteria": [
                "Evidence is attached or clearly referenced.",
                "Evidence has identifiable source system, owner, and date.",
                "Evidence resolves the stated gap.",
                "Reviewer validation notes document why closure is acceptable.",
                "Residual risk or exception is documented if evidence cannot be produced."
            ],
            "management_response": reg.get("management_response", ""),
            "closure_evidence": reg.get("closure_evidence", ""),
            "validation_notes": reg.get("validation_notes", "")
        })

    for row in register:
        readiness = _closure_readiness_score(row)
        closure_rows.append({
            **row,
            "closure_readiness_score": readiness["score"],
            "closure_readiness_rating": readiness["rating"],
            "closure_missing_steps": readiness["missing"],
            "closure_completed_steps": readiness["completed"]
        })

    avg_closure_readiness = round(sum(r["closure_readiness_score"] for r in closure_rows) / len(closure_rows)) if closure_rows else 0
    open_requests = len([r for r in request_rows if r.get("status") != "Closed"])
    closed_requests = len([r for r in request_rows if r.get("status") == "Closed"])

    return {
        "product": "Sentinel Evidence Request Studio",
        "version": "10.1.1",
        "generated_at": datetime.utcnow().isoformat(),
        "review_id": result.get("review_id"),
        "organization": result.get("organization"),
        "evidence_type": result.get("evidence_type"),
        "overall_rating": result.get("overall_rating"),
        "defensibility_score": result.get("evidence_defensibility_score"),
        "control_atlas_coverage_score": result.get("control_atlas_coverage_score"),
        "total_requests": len(request_rows),
        "open_requests": open_requests,
        "closed_requests": closed_requests,
        "average_closure_readiness_score": avg_closure_readiness,
        "owner_distribution": owner_counts,
        "priority_distribution": priority_counts,
        "status_distribution": status_counts,
        "evidence_requests": request_rows,
        "closure_readiness": closure_rows,
        "request_governance_note": (
            "Evidence requests should be tracked with accountable owner, target date, source artifact, management response, "
            "closure evidence, and reviewer validation notes. Closure should not be based on verbal confirmation alone."
        ),
        "request_operating_model": [
            "Send evidence request to the accountable evidence owner.",
            "Require source artifact, source system, reporting period, evidence date, and approval where applicable.",
            "Capture management response in the remediation register.",
            "Attach or reference closure evidence.",
            "Document reviewer validation notes before marking closed.",
            "Re-run Sentinel to confirm score improvement."
        ]
    }

def render_evidence_request_pack_html(pack: Dict[str, Any]) -> str:
    owner_rows = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
        for k, v in sorted(pack.get("owner_distribution", {}).items(), key=lambda x: x[1], reverse=True)
    )
    priority_rows = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
        for k, v in sorted(pack.get("priority_distribution", {}).items(), key=lambda x: x[1], reverse=True)
    )
    status_rows = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
        for k, v in sorted(pack.get("status_distribution", {}).items(), key=lambda x: x[1], reverse=True)
    )

    request_blocks = ""
    for req in pack.get("evidence_requests", []):
        artifacts = "".join(f"<li>{html.escape(str(a))}</li>" for a in req.get("preferred_artifacts", []))
        criteria = "".join(f"<li>{html.escape(str(c))}</li>" for c in req.get("closure_criteria", []))
        controls = ", ".join(req.get("control_atlas_ids", []))
        request_blocks += f"""
        <div class='request'>
          <h3>{html.escape(str(req.get('request_id','')))} · {html.escape(str(req.get('finding_id','')))} · {html.escape(str(req.get('priority','')))}</h3>
          <p><b>Owner:</b> {html.escape(str(req.get('owner','')))} | <b>Status:</b> {html.escape(str(req.get('status','')))} | <b>Target:</b> {html.escape(str(req.get('target_date','')))}</p>
          <p><b>Risk domain:</b> {html.escape(str(req.get('risk_domain','')))} | <b>Control Atlas:</b> {html.escape(controls)}</p>
          <p><b>Evidence Needed:</b> {html.escape(str(req.get('evidence_needed','')))}</p>
          <p><b>Request Message:</b> {html.escape(str(req.get('request_message','')))}</p>
          <h4>Preferred Artifacts</h4>
          <ul>{artifacts}</ul>
          <h4>Closure Criteria</h4>
          <ul>{criteria}</ul>
          <p><b>Validation Test:</b> {html.escape(str(req.get('validation_test','')))}</p>
        </div>
        """

    closure_rows = ""
    for row in pack.get("closure_readiness", []):
        missing = "; ".join(row.get("closure_missing_steps", []))
        closure_rows += f"""
        <tr>
          <td>{html.escape(str(row.get('finding_id','')))}</td>
          <td>{html.escape(str(row.get('severity','')))}</td>
          <td>{html.escape(str(row.get('owner','')))}</td>
          <td>{html.escape(str(row.get('status','')))}</td>
          <td>{row.get('closure_readiness_score','')}/100</td>
          <td>{html.escape(str(row.get('closure_readiness_rating','')))}</td>
          <td>{html.escape(missing)}</td>
        </tr>
        """

    operating_model = "".join(f"<li>{html.escape(x)}</li>" for x in pack.get("request_operating_model", []))

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Evidence Request Studio</title>
<style>
body {{ font-family: Arial, sans-serif; background:#f5f7fb; color:#111827; margin:0; padding:32px; }}
.pack {{ max-width:1280px; margin:auto; background:white; border-radius:22px; padding:38px; box-shadow:0 20px 70px rgba(15,23,42,.13); }}
.eyebrow {{ color:#1d4ed8; text-transform:uppercase; letter-spacing:.18em; font-size:12px; font-weight:800; }}
h1 {{ margin:8px 0 8px; font-size:40px; letter-spacing:-.04em; }}
.sub {{ color:#4b5563; }}
.cards {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin:24px 0; }}
.card {{ background:#f9fafb; border:1px solid #e5e7eb; border-radius:14px; padding:16px; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:23px; margin-top:6px; }}
.summary {{ border-left:5px solid #1d4ed8; background:#eff6ff; padding:16px; border-radius:12px; margin:18px 0; line-height:1.5; }}
.grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin:18px 0; }}
.panel, .request {{ border:1px solid #e5e7eb; border-radius:16px; padding:18px; margin:16px 0; background:#ffffff; }}
table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }}
th,td {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; vertical-align:top; }}
li {{ margin:7px 0; }}
.footer {{ color:#6b7280; font-size:12px; margin-top:24px; }}
@media print {{ body {{ background:white; padding:0; }} .pack {{ box-shadow:none; }} }}
</style>
</head>
<body>
<div class='pack'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Evidence Request Studio</h1>
<p class='sub'>Request-ready evidence pack with owners, priority, preferred artifacts, closure criteria, and validation tests.</p>

<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(str(pack.get('organization','')))}</strong></div>
<div class='card'><span>Total Requests</span><strong>{pack.get('total_requests','')}</strong></div>
<div class='card'><span>Open Requests</span><strong>{pack.get('open_requests','')}</strong></div>
<div class='card'><span>Closed</span><strong>{pack.get('closed_requests','')}</strong></div>
<div class='card'><span>Closure Readiness</span><strong>{pack.get('average_closure_readiness_score','')}/100</strong></div>
</div>

<div class='summary'>{html.escape(pack.get('request_governance_note',''))}</div>

<div class='grid'>
<div class='panel'><h2>Owners</h2><table><tr><th>Owner</th><th>Requests</th></tr>{owner_rows}</table></div>
<div class='panel'><h2>Priority</h2><table><tr><th>Priority</th><th>Requests</th></tr>{priority_rows}</table></div>
<div class='panel'><h2>Status</h2><table><tr><th>Status</th><th>Requests</th></tr>{status_rows}</table></div>
</div>

<div class='panel'><h2>Operating Model</h2><ol>{operating_model}</ol></div>

<h2>Evidence Requests</h2>
{request_blocks}

<h2>Closure Readiness Tracker</h2>
<table><tr><th>Finding</th><th>Severity</th><th>Owner</th><th>Status</th><th>Readiness</th><th>Rating</th><th>Missing Steps</th></tr>{closure_rows}</table>

<div class='footer'>Generated by Sentinel Evidence Defensibility Workbench v7.0. This output supports evidence follow-up, remediation closure, and management response tracking.</div>
</div>
</body>
</html>"""

@app.get("/api/reviews/{review_id}/request-studio")
def saved_review_request_studio(review_id: str):
    result = get_review(review_id)
    return build_evidence_request_studio_pack(result)

@app.get("/api/reviews/{review_id}/request-studio-html", response_class=HTMLResponse)
def saved_review_request_studio_html(review_id: str):
    result = get_review(review_id)
    return render_evidence_request_pack_html(build_evidence_request_studio_pack(result))


def build_demo_room_pack(result: Dict[str, Any]) -> Dict[str, Any]:
    board = build_board_pack_from_result(result)
    request_pack = build_evidence_request_studio_pack(result)

    defensibility = result.get("evidence_defensibility_score") or 0
    control_atlas = result.get("control_atlas_coverage_score") or 0
    closure = request_pack.get("average_closure_readiness_score") or 0
    metadata = result.get("metadata_completeness_score") or 0
    readiness = round((defensibility * 0.30) + (control_atlas * 0.30) + (closure * 0.20) + (metadata * 0.20))

    if readiness >= 80:
        demo_status = "Demo-ready"
    elif readiness >= 60:
        demo_status = "Usable with explanation"
    else:
        demo_status = "Use as gap-discovery demo"

    one_liner = (
        "Sentinel is an evidence defensibility workbench for GRC, audit, risk, privacy, TPRM, SDLC, IAM, and AI governance teams "
        "that challenges whether evidence is reliable enough for audit, regulator, or management reliance."
    )

    buyer_value_matrix = [
        {
            "buyer": "CISO / Security Leadership",
            "pain": "Evidence exists across teams but is inconsistent, screenshot-heavy, and hard to defend during audits.",
            "value": "Gives leadership a defensibility score, recurring risk themes, and board-ready remediation narrative.",
            "demo_moment": "Show Board Pack and Portfolio risk roll-up."
        },
        {
            "buyer": "IT GRC / 2LOD",
            "pain": "Manual credible challenge takes too long and follow-up requests are inconsistent.",
            "value": "Converts gaps into control-mapped evidence requests, challenge questions, and closure criteria.",
            "demo_moment": "Show Control Atlas and Evidence Request Studio."
        },
        {
            "buyer": "Internal Audit",
            "pain": "Audit evidence quality varies and workpapers need better source lineage and review trails.",
            "value": "Highlights source lineage, calculation integrity, approval evidence, and closure readiness.",
            "demo_moment": "Show finding severity rationale and closure readiness scoring."
        },
        {
            "buyer": "TPRM / Privacy",
            "pain": "SOC 2 reliance, CUEC analysis, data flow, retention, and privacy evidence are often incomplete.",
            "value": "Creates missing-artifact lists and owner-ready requests for vendor/privacy follow-up.",
            "demo_moment": "Run the Vendor Privacy sample package."
        }
    ]

    demo_flow = [
        {
            "step": "1",
            "screen": "Evidence Intake",
            "action": "Load a sample package or upload JSON/CSV evidence.",
            "talk_track": "We start where teams actually struggle: scattered evidence packages, not clean system integrations.",
            "proof_point": "Sentinel accepts lightweight evidence packages and structures them for review."
        },
        {
            "step": "2",
            "screen": "Run + Save Review",
            "action": "Click Run + Save Review to Vault.",
            "talk_track": "The first output is not a policy checklist. It is a defensibility review of whether evidence can withstand challenge.",
            "proof_point": "Scores are created for defensibility, metadata, intake, and control coverage."
        },
        {
            "step": "3",
            "screen": "Control Atlas",
            "action": "Open Control Atlas tab.",
            "talk_track": "Every gap is tied back to a control objective, expected artifacts, and challenge questions.",
            "proof_point": "This converts subjective review into a structured assurance conversation."
        },
        {
            "step": "4",
            "screen": "Evidence Requests",
            "action": "Open Evidence Requests tab and copy a request.",
            "talk_track": "Sentinel turns findings into owner-ready follow-up requests, not just dashboards.",
            "proof_point": "The request includes owner, priority, preferred artifacts, closure criteria, and validation test."
        },
        {
            "step": "5",
            "screen": "Command Center",
            "action": "Add owner, target date, management response, closure evidence, and validation notes.",
            "talk_track": "This is the operating workflow: finding to response to closure readiness.",
            "proof_point": "Closure readiness improves when management response and evidence fields are completed."
        },
        {
            "step": "6",
            "screen": "Board Pack",
            "action": "Open Board Pack tab.",
            "talk_track": "Leadership does not want raw findings. They need what to ask, what to fix, and what evidence blocks closure.",
            "proof_point": "Sentinel generates executive narrative, board questions, and 30-day action plan."
        },
        {
            "step": "7",
            "screen": "Portfolio",
            "action": "Show portfolio view and export portfolio board pack.",
            "talk_track": "Across reviews, Sentinel shows recurring risk domains and control concentration.",
            "proof_point": "This is how the tool moves from one review to evidence assurance portfolio oversight."
        }
    ]

    objection_handling = [
        {
            "objection": "Is this replacing GRC tools?",
            "response": "No. Sentinel is a defensibility challenge layer. It can sit before or beside Archer, ServiceNow, Jira, Sheets, or audit workpapers."
        },
        {
            "objection": "Is this production SaaS today?",
            "response": "The current build is a local Final Edition/demo. Production needs authentication, PostgreSQL, tenant isolation, audit logs, and deployment hardening."
        },
        {
            "objection": "Why not just use spreadsheets?",
            "response": "Spreadsheets track rows. Sentinel structures the reasoning: evidence gap, control objective, missing artifact, request message, and closure test."
        },
        {
            "objection": "Is the current engine real AI?",
            "response": "The current Final Edition uses deterministic scoring and structured logic. The next production-grade step is adding AI-assisted narrative and evidence interpretation under controlled prompts."
        }
    ]

    pilot_offer = {
        "name": "Evidence Defensibility Sprint",
        "duration": "2 weeks",
        "scope": [
            "Review 10-25 evidence packages across one process area.",
            "Generate defensibility scores, findings, missing evidence, and request tracker.",
            "Deliver board-style summary and remediation register.",
            "Run one readout session with owners and risk/compliance stakeholders."
        ],
        "ideal_client": "Banks, fintechs, BFSI GCCs, audit teams, IT GRC teams, TPRM teams, and AI governance teams.",
        "success_metric": "Evidence packages move from unclear/unreliable to owner-assigned, artifact-specific, and closure-ready."
    }

    next_build_recommendation = [
        "Freeze this as Executive Demo Edition.",
        "Clean code structure before adding more features.",
        "Add OpenAI-assisted narrative after demo flow is stable.",
        "Move SQLite to PostgreSQL before external deployment.",
        "Design final 4-5 screens in Figma before UI expansion."
    ]

    return {
        "product": "Sentinel Executive Demo Room",
        "version": "10.1.1",
        "generated_at": datetime.utcnow().isoformat(),
        "review_id": result.get("review_id"),
        "organization": result.get("organization"),
        "evidence_type": result.get("evidence_type"),
        "demo_readiness_score": readiness,
        "demo_status": demo_status,
        "one_liner": one_liner,
        "positioning": "Not a GRC repository. A defensibility challenge layer for evidence, controls, and closure readiness.",
        "core_workflow": "Evidence → Defensibility Review → Control Atlas → Evidence Request → Management Response → Closure Readiness → Board Pack → Portfolio Oversight",
        "buyer_value_matrix": buyer_value_matrix,
        "demo_flow": demo_flow,
        "objection_handling": objection_handling,
        "pilot_offer": pilot_offer,
        "next_build_recommendation": next_build_recommendation,
        "board_pack_snapshot": {
            "overall_rating": board.get("overall_rating"),
            "defensibility_score": board.get("evidence_defensibility_score"),
            "control_atlas_coverage_score": board.get("control_atlas_coverage_score"),
            "high_or_critical_findings": board.get("high_or_critical_findings"),
            "open_register_items": board.get("open_register_items"),
            "top_missing_evidence": board.get("top_missing_evidence", [])[:8],
            "board_questions": board.get("board_questions", [])[:5]
        },
        "request_pack_snapshot": {
            "total_requests": request_pack.get("total_requests"),
            "open_requests": request_pack.get("open_requests"),
            "average_closure_readiness_score": request_pack.get("average_closure_readiness_score"),
            "owner_distribution": request_pack.get("owner_distribution"),
            "priority_distribution": request_pack.get("priority_distribution")
        }
    }

def render_demo_room_html(pack: Dict[str, Any]) -> str:
    demo_rows = ""
    for step in pack.get("demo_flow", []):
        demo_rows += f"""
        <div class='step'>
          <h3>{html.escape(step.get('step',''))}. {html.escape(step.get('screen',''))}</h3>
          <p><b>Action:</b> {html.escape(step.get('action',''))}</p>
          <p><b>Talk track:</b> {html.escape(step.get('talk_track',''))}</p>
          <p><b>Proof point:</b> {html.escape(step.get('proof_point',''))}</p>
        </div>
        """

    buyer_rows = ""
    for row in pack.get("buyer_value_matrix", []):
        buyer_rows += f"""
        <tr>
          <td>{html.escape(row.get('buyer',''))}</td>
          <td>{html.escape(row.get('pain',''))}</td>
          <td>{html.escape(row.get('value',''))}</td>
          <td>{html.escape(row.get('demo_moment',''))}</td>
        </tr>
        """

    objection_rows = ""
    for row in pack.get("objection_handling", []):
        objection_rows += f"<tr><td>{html.escape(row.get('objection',''))}</td><td>{html.escape(row.get('response',''))}</td></tr>"

    pilot = pack.get("pilot_offer", {})
    scope = "".join(f"<li>{html.escape(x)}</li>" for x in pilot.get("scope", []))
    next_build = "".join(f"<li>{html.escape(x)}</li>" for x in pack.get("next_build_recommendation", []))
    board_questions = "".join(f"<li>{html.escape(x)}</li>" for x in pack.get("board_pack_snapshot", {}).get("board_questions", []))
    missing = "".join(f"<li>{html.escape(x.get('artifact',''))} — {x.get('count')}</li>" for x in pack.get("board_pack_snapshot", {}).get("top_missing_evidence", []))

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Executive Demo Room</title>
<style>
body {{ font-family: Arial, sans-serif; background:#f5f7fb; color:#111827; margin:0; padding:32px; }}
.pack {{ max-width:1280px; margin:auto; background:white; border-radius:22px; padding:38px; box-shadow:0 20px 70px rgba(15,23,42,.13); }}
.eyebrow {{ color:#1d4ed8; text-transform:uppercase; letter-spacing:.18em; font-size:12px; font-weight:800; }}
h1 {{ margin:8px 0 8px; font-size:42px; letter-spacing:-.04em; }}
.sub {{ color:#4b5563; }}
.cards {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin:24px 0; }}
.card {{ background:#f9fafb; border:1px solid #e5e7eb; border-radius:14px; padding:16px; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:23px; margin-top:6px; }}
.summary {{ border-left:5px solid #1d4ed8; background:#eff6ff; padding:16px; border-radius:12px; margin:18px 0; line-height:1.5; }}
.step, .panel {{ border:1px solid #e5e7eb; border-radius:16px; padding:18px; margin:16px 0; background:#ffffff; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }}
th,td {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; vertical-align:top; }}
li {{ margin:7px 0; }}
.footer {{ color:#6b7280; font-size:12px; margin-top:24px; }}
@media print {{ body {{ background:white; padding:0; }} .pack {{ box-shadow:none; }} }}
</style>
</head>
<body>
<div class='pack'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Executive Demo Room</h1>
<p class='sub'>Final Final Edition demo script, buyer narrative, pilot offer, objection handling, and build boundary.</p>

<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(str(pack.get('organization','')))}</strong></div>
<div class='card'><span>Demo Readiness</span><strong>{pack.get('demo_readiness_score','')}/100</strong></div>
<div class='card'><span>Status</span><strong>{html.escape(str(pack.get('demo_status','')))}</strong></div>
<div class='card'><span>Version</span><strong>{html.escape(str(pack.get('version','')))}</strong></div>
</div>

<div class='summary'><b>One-liner:</b> {html.escape(pack.get('one_liner',''))}</div>
<div class='summary'><b>Positioning:</b> {html.escape(pack.get('positioning',''))}</div>
<div class='summary'><b>Workflow:</b> {html.escape(pack.get('core_workflow',''))}</div>

<h2>Buyer Value Matrix</h2>
<table><tr><th>Buyer</th><th>Pain</th><th>Value</th><th>Demo Moment</th></tr>{buyer_rows}</table>

<h2>Seven-Step Demo Flow</h2>
{demo_rows}

<div class='grid'>
<div class='panel'><h2>Board Questions</h2><ol>{board_questions}</ol></div>
<div class='panel'><h2>Top Missing Evidence</h2><ol>{missing}</ol></div>
</div>

<h2>Objection Handling</h2>
<table><tr><th>Objection</th><th>Response</th></tr>{objection_rows}</table>

<div class='panel'>
<h2>{html.escape(pilot.get('name','Pilot Offer'))}</h2>
<p><b>Duration:</b> {html.escape(str(pilot.get('duration','')))}</p>
<p><b>Ideal client:</b> {html.escape(str(pilot.get('ideal_client','')))}</p>
<p><b>Success metric:</b> {html.escape(str(pilot.get('success_metric','')))}</p>
<h3>Scope</h3>
<ul>{scope}</ul>
</div>

<div class='panel'><h2>Next Build Recommendation</h2><ol>{next_build}</ol></div>

<div class='footer'>Generated by Sentinel Evidence Defensibility Workbench v10.1. This is an executive-demo package, not a production SaaS certification.</div>
</div>
</body>
</html>"""

@app.get("/api/reviews/{review_id}/demo-room")
def saved_review_demo_room(review_id: str):
    result = get_review(review_id)
    return build_demo_room_pack(result)

@app.get("/api/reviews/{review_id}/demo-room-html", response_class=HTMLResponse)
def saved_review_demo_room_html(review_id: str):
    result = get_review(review_id)
    return render_demo_room_html(build_demo_room_pack(result))

@app.get("/api/portfolio/demo-room-html", response_class=HTMLResponse)
def portfolio_demo_room_html():
    snapshot = portfolio_dashboard()
    narrative = (
        f"Sentinel portfolio currently contains {snapshot.get('total_reviews')} saved review(s), "
        f"{snapshot.get('total_findings')} finding(s), and {snapshot.get('open_register_items')} open remediation item(s). "
        f"The average defensibility score is {snapshot.get('average_defensibility_score')}/100."
    )
    domain_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot.get('risk_domain_distribution', {}).items(), key=lambda x: x[1], reverse=True))
    control_rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>" for k, v in sorted(snapshot.get('control_atlas_distribution', {}).items(), key=lambda x: x[1], reverse=True))
    return f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>Sentinel Portfolio Demo Room</title>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#111827;margin:0;padding:32px}}
.pack{{max-width:1180px;margin:auto;background:white;border-radius:22px;padding:38px;box-shadow:0 20px 70px rgba(15,23,42,.13)}}
.eyebrow{{color:#1d4ed8;text-transform:uppercase;letter-spacing:.18em;font-size:12px;font-weight:800}}
h1{{font-size:40px;margin:8px 0}}.summary{{border-left:5px solid #1d4ed8;background:#eff6ff;padding:16px;border-radius:12px;margin:18px 0;line-height:1.5}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.panel{{border:1px solid #e5e7eb;border-radius:16px;padding:18px}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}}td,th{{border-bottom:1px solid #e5e7eb;padding:10px;text-align:left}}
</style></head>
<body><div class='pack'><div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div><h1>Portfolio Demo Room</h1><div class='summary'>{html.escape(narrative)}</div>
<div class='grid'><div class='panel'><h2>Risk Domains</h2><table><tr><th>Domain</th><th>Count</th></tr>{domain_rows}</table></div><div class='panel'><h2>Control Concentration</h2><table><tr><th>Control</th><th>Count</th></tr>{control_rows}</table></div></div>
</div></body></html>"""


FINAL_RELEASE = {
    "product_name": "Sentinel Evidence Defensibility Workbench",
    "company": "Eye On Bits Pvt Ltd",
    "version": "10.1.1",
    "status": "Final launch baseline",
    "positioning": "Sentinel is not a GRC repository. It is an evidence defensibility challenge layer for audit, risk, compliance, TPRM, privacy, SDLC, IAM, and AI governance reviews.",
    "one_liner": "Sentinel turns weak evidence packages into findings, evidence requests, control mappings, board-ready narratives, and closure-ready remediation workflows.",
    "final_in_scope": [
        "Evidence package intake using JSON, CSV, TXT, and MD",
        "Evidence defensibility scoring",
        "Persistent local review vault",
        "Control Atlas mapping",
        "Evidence Request Studio",
        "Closure Readiness Engine",
        "Board Pack Studio",
        "Executive Demo Room",
        "Delivery Kit",
        "Portfolio dashboard",
        "HTML, JSON, and CSV exports",
        "Local Docker-based execution"
    ],
    "explicitly_out_of_scope_for_final": [
        "Production authentication and RBAC",
        "Multi-tenant SaaS deployment",
        "Enterprise encryption and key management",
        "Formal AI model reasoning with LLM API calls",
        "PostgreSQL production database",
        "Workflow approvals and email automation",
        "SOC 2-ready infrastructure controls",
        "Legal/regulatory advice"
    ],
    "next_versions_only_if_justified": [
        {"version": "Next Stage A", "gate": "Real OpenAI reasoning layer with evidence narrative generation and explainable prompt logging"},
        {"version": "Next Stage B", "gate": "PostgreSQL, authentication, users, and hosted deployment"},
        {"version": "Next Stage C", "gate": "n8n / Google Workspace automation for evidence request follow-ups"}
    ],
    "pilot_offer": {
        "name": "Evidence Defensibility Sprint",
        "duration": "2 weeks",
        "buyer": "IT GRC, Internal Audit, TPRM, Privacy, SDLC Governance, IAM, AI Governance teams",
        "deliverables": [
            "Evidence defensibility review",
            "Finding register",
            "Evidence request list",
            "Control Atlas mapping",
            "Board-ready summary",
            "Closure readiness tracker",
            "Remediation action plan"
        ]
    }
}

@app.get("/api/product/freeze")
def product_freeze():
    return FINAL_RELEASE

@app.get("/api/product/final-scope")
def product_final_scope():
    return FINAL_RELEASE

@app.get("/api/vault/export")
def export_vault():
    ensure_db()
    with db() as conn:
        rows = conn.execute("SELECT * FROM reviews ORDER BY created_at DESC").fetchall()

    exported = []
    for row in rows:
        exported.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "organization": row["organization"],
            "industry": row["industry"],
            "evidence_type": row["evidence_type"],
            "review_objective": row["review_objective"],
            "overall_rating": row["overall_rating"],
            "evidence_defensibility_score": row["evidence_defensibility_score"],
            "intake_coverage_score": row["intake_coverage_score"],
            "metadata_completeness_score": row["metadata_completeness_score"],
            "total_findings": row["total_findings"],
            "payload": json.loads(row["payload_json"]),
            "result": json.loads(row["result_json"]),
            "register": json.loads(row["register_json"])
        })

    return {
        "product": "Sentinel Evidence Defensibility Workbench",
        "version": "10.1.1",
        "exported_at": datetime.utcnow().isoformat(),
        "review_count": len(exported),
        "reviews": exported
    }

@app.get("/api/launch/readiness")
def launch_readiness():
    portfolio = portfolio_dashboard()
    freeze = FINAL_RELEASE

    readiness_items = [
        {"item": "Product positioning defined", "status": "Ready", "evidence": freeze["positioning"]},
        {"item": "Final product scope frozen", "status": "Ready", "evidence": f"{len(freeze['final_in_scope'])} in-scope capabilities"},
        {"item": "Out-of-scope boundaries defined", "status": "Ready", "evidence": f"{len(freeze['explicitly_out_of_scope_for_final'])} exclusions"},
        {"item": "Saved review vault available", "status": "Ready" if portfolio.get("total_reviews", 0) > 0 else "Pending", "evidence": f"{portfolio.get('total_reviews', 0)} saved review(s)"},
        {"item": "Portfolio dashboard available", "status": "Ready", "evidence": "Portfolio API active"},
        {"item": "Board pack available", "status": "Ready", "evidence": "Board Pack Studio endpoint active"},
        {"item": "Evidence request workflow available", "status": "Ready", "evidence": "Evidence Request Studio endpoint active"},
        {"item": "Export capability available", "status": "Ready", "evidence": "HTML, JSON, CSV exports available"},
        {"item": "Pilot offer defined", "status": "Ready", "evidence": freeze["pilot_offer"]["name"]},
        {"item": "Production security boundary documented", "status": "Ready", "evidence": "Final Edition is local demo-grade software, not production SaaS"}
    ]

    ready_count = len([x for x in readiness_items if x["status"] == "Ready"])
    score = round((ready_count / len(readiness_items)) * 100)

    return {
        "product": freeze["product_name"],
        "version": "10.1.1",
        "status": "Final launch baseline",
        "launch_readiness_score": score,
        "generated_at": datetime.utcnow().isoformat(),
        "readiness_items": readiness_items,
        "portfolio_snapshot": portfolio,
        "final": freeze,
        "freeze": freeze
    }

@app.get("/api/launch/readiness-html", response_class=HTMLResponse)
def launch_readiness_html():
    readiness = launch_readiness()
    freeze = readiness["freeze"]
    portfolio = readiness["portfolio_snapshot"]

    readiness_rows = "".join(
        f"<tr><td>{html.escape(x['item'])}</td><td>{html.escape(x['status'])}</td><td>{html.escape(str(x['evidence']))}</td></tr>"
        for x in readiness["readiness_items"]
    )

    scope_rows = "".join(f"<li>{html.escape(x)}</li>" for x in freeze["final_in_scope"])
    exclusion_rows = "".join(f"<li>{html.escape(x)}</li>" for x in freeze["explicitly_out_of_scope_for_final"])
    deliverable_rows = "".join(f"<li>{html.escape(x)}</li>" for x in freeze["pilot_offer"]["deliverables"])

    roadmap_rows = "".join(
        f"<tr><td>{html.escape(x['version'])}</td><td>{html.escape(x['gate'])}</td></tr>"
        for x in freeze["next_versions_only_if_justified"]
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel v10.1.1 Final Launch Edition Report</title>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#111827;margin:0;padding:32px}}
.report{{max-width:1280px;margin:auto;background:white;border-radius:22px;padding:38px;box-shadow:0 20px 70px rgba(15,23,42,.13)}}
.eyebrow{{color:#1d4ed8;text-transform:uppercase;letter-spacing:.18em;font-size:12px;font-weight:800}}
h1{{margin:8px 0;font-size:42px;letter-spacing:-.04em}}.sub{{color:#4b5563;line-height:1.5}}
.cards{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:24px 0}}
.card{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:14px;padding:16px}}
.card span{{display:block;color:#6b7280;font-size:12px;text-transform:uppercase}}.card strong{{display:block;font-size:23px;margin-top:6px}}
.summary{{border-left:5px solid #1d4ed8;background:#eff6ff;padding:16px;border-radius:12px;margin:18px 0;line-height:1.5}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.panel{{border:1px solid #e5e7eb;border-radius:16px;padding:18px;margin:16px 0;background:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}}th,td{{border-bottom:1px solid #e5e7eb;padding:10px;text-align:left;vertical-align:top}}li{{margin:7px 0}}
@media print{{body{{background:white;padding:0}}.report{{box-shadow:none}}}}
</style>
</head>
<body>
<div class='report'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Final Launch Edition Report</h1>
<p class='sub'>{html.escape(freeze['positioning'])}</p>
<div class='cards'>
<div class='card'><span>Launch Readiness</span><strong>{readiness['launch_readiness_score']}/100</strong></div>
<div class='card'><span>Status</span><strong>Final Edition Frozen</strong></div>
<div class='card'><span>Saved Reviews</span><strong>{portfolio.get('total_reviews',0)}</strong></div>
<div class='card'><span>Total Findings</span><strong>{portfolio.get('total_findings',0)}</strong></div>
<div class='card'><span>Open Items</span><strong>{portfolio.get('open_register_items',0)}</strong></div>
</div>
<div class='summary'><b>One-liner:</b> {html.escape(freeze['one_liner'])}</div>
<h2>Readiness Checklist</h2>
<table><tr><th>Item</th><th>Status</th><th>Evidence</th></tr>{readiness_rows}</table>
<div class='grid'>
<div class='panel'><h2>Final Edition Scope</h2><ul>{scope_rows}</ul></div>
<div class='panel'><h2>Out of Scope for Final Edition</h2><ul>{exclusion_rows}</ul></div>
</div>
<div class='panel'><h2>Pilot Offer: {html.escape(freeze['pilot_offer']['name'])}</h2><p><b>Duration:</b> {html.escape(freeze['pilot_offer']['duration'])}</p><p><b>Buyer:</b> {html.escape(freeze['pilot_offer']['buyer'])}</p><ul>{deliverable_rows}</ul></div>
<h2>Future Versions: Only If Justified</h2>
<table><tr><th>Version</th><th>Gate</th></tr>{roadmap_rows}</table>
</div>
</body>
</html>"""


FINAL_RELEASE_MANIFEST = {
    "product_name": "Sentinel Evidence Defensibility Workbench",
    "company": "Eye On Bits Pvt Ltd",
    "version": "10.1.1",
    "edition": "Final Launch Edition",
    "release_status": "Feature baseline complete",
    "positioning": "Sentinel is an evidence defensibility challenge layer for audit, risk, compliance, TPRM, privacy, SDLC, IAM, and AI governance reviews.",
    "one_liner": "Sentinel turns weak evidence packages into findings, evidence requests, control mappings, board-ready narratives, and closure-ready remediation workflows.",
    "capability_stack": [
        "Evidence intake",
        "Evidence defensibility scoring",
        "Persistent local review vault",
        "Control Atlas mapping",
        "Evidence Request Studio",
        "Closure Readiness Engine",
        "Board Pack Studio",
        "Executive Demo Room",
        "Delivery Kit",
        "Launch Room",
        "Portfolio dashboard",
        "HTML, JSON, and CSV exports",
        "Docker-based local execution"
    ],
    "commercial_offer": {
        "name": "Evidence Defensibility Sprint",
        "duration": "2 weeks",
        "outcome": "Find weak evidence before audit, examiners, management committees, or 2LOD credible challenge expose it.",
        "deliverables": [
            "Evidence defensibility review",
            "Finding register",
            "Evidence request list",
            "Control Atlas mapping",
            "Board-ready summary",
            "Closure readiness tracker",
            "Remediation action plan",
            "Client delivery kit"
        ]
    },
    "important_boundary": "This edition is a local demo-grade product baseline. Production use requires authentication, authorization, hardened deployment, data protection controls, secure secrets management, monitoring, and formal legal/security review.",
    "next_stage_gates": [
        {"stage": "AI Reasoning Layer", "condition": "Add real OpenAI-assisted reasoning with prompt logging and evidence-grounded outputs."},
        {"stage": "Hosted Product Layer", "condition": "Add PostgreSQL, authentication, user accounts, tenant boundaries, and deployment hardening."},
        {"stage": "Automation Layer", "condition": "Add n8n / Google Workspace workflows for evidence owner follow-up and tracker updates."}
    ]
}

@app.get("/api/product/final-release")
def final_release_manifest():
    return FINAL_RELEASE_MANIFEST

@app.get("/api/product/final-release-html", response_class=HTMLResponse)
def final_release_manifest_html():
    cap_rows = "".join(f"<li>{html.escape(x)}</li>" for x in FINAL_RELEASE_MANIFEST["capability_stack"])
    deliv_rows = "".join(f"<li>{html.escape(x)}</li>" for x in FINAL_RELEASE_MANIFEST["commercial_offer"]["deliverables"])
    gates = "".join(
        f"<tr><td>{html.escape(x['stage'])}</td><td>{html.escape(x['condition'])}</td></tr>"
        for x in FINAL_RELEASE_MANIFEST["next_stage_gates"]
    )
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel v10 Final Launch Edition</title>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fb;color:#111827;margin:0;padding:32px}}
.report{{max-width:1180px;margin:auto;background:white;border-radius:22px;padding:38px;box-shadow:0 20px 70px rgba(15,23,42,.13)}}
.eyebrow{{color:#1d4ed8;text-transform:uppercase;letter-spacing:.18em;font-size:12px;font-weight:800}}
h1{{margin:8px 0;font-size:42px;letter-spacing:-.04em}}
.summary{{border-left:5px solid #1d4ed8;background:#eff6ff;padding:16px;border-radius:12px;margin:18px 0;line-height:1.5}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.panel{{border:1px solid #e5e7eb;border-radius:16px;padding:18px;margin:16px 0;background:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}}th,td{{border-bottom:1px solid #e5e7eb;padding:10px;text-align:left;vertical-align:top}}li{{margin:7px 0}}
</style>
</head>
<body>
<div class='report'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v10.1.1</div>
<h1>Final Launch Edition</h1>
<div class='summary'><b>Positioning:</b> {html.escape(FINAL_RELEASE_MANIFEST['positioning'])}</div>
<div class='summary'><b>One-liner:</b> {html.escape(FINAL_RELEASE_MANIFEST['one_liner'])}</div>
<div class='grid'><div class='panel'><h2>Capability Stack</h2><ul>{cap_rows}</ul></div><div class='panel'><h2>Commercial Offer</h2><p><b>{html.escape(FINAL_RELEASE_MANIFEST['commercial_offer']['name'])}</b> · {html.escape(FINAL_RELEASE_MANIFEST['commercial_offer']['duration'])}</p><p>{html.escape(FINAL_RELEASE_MANIFEST['commercial_offer']['outcome'])}</p><ul>{deliv_rows}</ul></div></div>
<div class='panel'><h2>Important Boundary</h2><p>{html.escape(FINAL_RELEASE_MANIFEST['important_boundary'])}</p></div>
<h2>Next Stage Gates</h2><table><tr><th>Stage</th><th>Condition</th></tr>{gates}</table>
</div>
</body>
</html>"""
