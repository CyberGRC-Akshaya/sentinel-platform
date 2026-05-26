
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
    description="Professional assurance workbench with persistent review vault, portfolio analytics, remediation register, and executive reporting exports.",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    {
        "key": "source_lineage",
        "label": "Source Lineage",
        "weight": 18,
        "positive": ["source export", "system export", "source-of-record", "source of record", "query", "extract", "timestamp", "api export"],
        "negative": ["screenshot-only", "screenshot only", "manual", "email screenshot", "corrected later"]
    },
    {
        "key": "completeness",
        "label": "Completeness",
        "weight": 16,
        "positive": ["population", "complete", "full extract", "all records", "reconciliation", "tie-out", "scope boundary"],
        "negative": ["partial", "sample only", "not included", "missing", "not available", "does not include", "not provided"]
    },
    {
        "key": "calculation_integrity",
        "label": "Calculation Integrity",
        "weight": 16,
        "positive": ["numerator", "denominator", "formula", "calculation", "logic", "recalculation", "validated"],
        "negative": ["changed to", "mismatch", "inconsistent", "corrected later", "cumulative", "unclear", "manual adjustment"]
    },
    {
        "key": "review_approval",
        "label": "Review & Approval Evidence",
        "weight": 14,
        "positive": ["approved", "reviewed", "sign-off", "sign off", "attested", "owner approval", "review notes"],
        "negative": ["no approval", "not approved", "no review", "review not shown", "owner stated", "verbal confirmation"]
    },
    {
        "key": "period_alignment",
        "label": "Reporting Period Alignment",
        "weight": 12,
        "positive": ["q1", "q2", "q3", "q4", "monthly", "quarterly", "annual", "reporting period", "as of", "period end"],
        "negative": ["year-to-date", "ytd", "cumulative", "prior period", "unclear period", "mixed period"]
    },
    {
        "key": "governance_traceability",
        "label": "Governance Traceability",
        "weight": 14,
        "positive": ["policy", "standard", "control", "risk acceptance", "exception", "issue", "ticket", "change record", "jira", "servicenow"],
        "negative": ["no ticket", "no change record", "no exception", "no risk acceptance", "not documented"]
    },
    {
        "key": "data_handling",
        "label": "Data Handling & Privacy Boundary",
        "weight": 10,
        "positive": ["data flow", "retention", "pii", "npi", "customer data", "encryption", "access boundary", "dpa", "deletion"],
        "negative": ["no data flow", "retention not", "unknown retention", "no dpa", "unknown processing"]
    }
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
        conn.execute(
            """
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
            """
        )
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
        "title": item.title,
        "domain": domain,
        "artifact_type": artifact_type,
        "has_owner": bool(item.owner),
        "has_source_system": bool(item.source_system),
        "has_reporting_period": bool(item.reporting_period),
        "has_control_reference": bool(item.control_reference),
        "has_evidence_date": bool(item.evidence_date),
        "text_length": len(item.content or ""),
        "metadata_completeness_score": 0,
        "missing_metadata": []
    }

    checks = [
        ("has_owner", "owner"),
        ("has_source_system", "source_system"),
        ("has_reporting_period", "reporting_period"),
        ("has_control_reference", "control_reference"),
        ("has_evidence_date", "evidence_date")
    ]

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
    present = []
    missing = []

    for requirement in requirements:
        if requirement.lower() in text:
            present.append(requirement)
        else:
            missing.append(requirement)

    coverage = round((len(present) / len(requirements)) * 100) if requirements else 0
    rating = "Strong Intake" if coverage >= 80 else "Partial Intake" if coverage >= 55 else "Weak Intake"

    return {
        "title": item.title,
        "domain": domain,
        "required_evidence_elements": requirements,
        "present_elements": present,
        "missing_elements": missing,
        "intake_coverage_score": coverage,
        "intake_rating": rating
    }

def dimension_score(text: str, dimension: Dict[str, Any]) -> Dict[str, Any]:
    base = 65
    positive_hits = [p for p in dimension["positive"] if p in text]
    negative_hits = [n for n in dimension["negative"] if n in text]
    score = max(0, min(100, base + (len(positive_hits) * 8) - (len(negative_hits) * 12)))
    rating = "Strong" if score >= 80 else "Moderate" if score >= 60 else "Weak" if score >= 40 else "Deficient"

    return {
        "key": dimension["key"],
        "label": dimension["label"],
        "weight": dimension["weight"],
        "score": score,
        "rating": rating,
        "positive_indicators": positive_hits,
        "negative_indicators": negative_hits
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
        "artifact_profile": infer_artifact_profile(item, domain)
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

    preferred = {
        "source_lineage": ["source-of-record extract", "query/filter criteria", "timestamped export", "extract owner evidence"],
        "completeness": ["population report", "reconciliation", "scope definition", "sample basis if sampling was used"],
        "calculation_integrity": ["metric definition", "formula", "numerator/denominator support", "independent recalculation"],
        "review_approval": ["review notes", "approval record", "control owner sign-off", "committee approval where applicable"],
        "period_alignment": ["reporting calendar", "as-of date evidence", "period-specific extract", "committee reporting tie-out"],
        "governance_traceability": ["ticket/change record", "risk acceptance", "exception approval", "issue/remediation tracker"],
        "data_handling": ["data-flow diagram", "retention evidence", "access boundary evidence", "contractual/privacy obligation"]
    }

    request = {
        "request_id": f"REQ-{idx:03d}",
        "evidence_needed": f"Provide evidence supporting {dimension['label'].lower()} for {item.title}.",
        "preferred_artifacts": preferred.get(dimension["key"], ["supporting evidence package"]),
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

    if not findings:
        domain = item_scores[0]["domain"] if item_scores else "General Evidence Defensibility"
        findings.append(build_finding(
            EvidenceItem(title="Overall Evidence Package", content="General positive review", owner="Evidence Owner"),
            {"domain": domain},
            {"key": "general", "label": "General Review", "score": 85, "rating": "Strong", "positive_indicators": ["general"], "negative_indicators": []},
            1
        ))

    overall_score = round(sum(i["score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    intake_score = round(sum(i["intake_gap_analysis"]["intake_coverage_score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    metadata_score = round(sum(i["artifact_profile"]["metadata_completeness_score"] for i in item_scores) / len(item_scores)) if item_scores else 0
    rating = "Strong" if overall_score >= 85 else "Moderate" if overall_score >= 70 else "Weak" if overall_score >= 50 else "Critical Attention Required"

    severity_distribution: Dict[str, int] = {}
    domain_counts: Dict[str, int] = {}
    framework_counts: Dict[str, int] = {}

    for finding in findings:
        severity_distribution[finding["severity"]] = severity_distribution.get(finding["severity"], 0) + 1
        domain_counts[finding["risk_domain"]] = domain_counts.get(finding["risk_domain"], 0) + 1
        for fw in finding["framework_relevance"]:
            framework_counts[fw] = framework_counts.get(fw, 0) + 1

    evidence_requests = [f["evidence_request"] for f in findings]
    executive_summary = (
        f"Sentinel reviewed {len(payload.items)} evidence item(s). The package is rated '{rating}' "
        f"with an evidence defensibility score of {overall_score}/100, intake coverage score of {intake_score}/100, "
        f"and metadata completeness score of {metadata_score}/100. {len(findings)} finding(s) and "
        f"{len(evidence_requests)} evidence request(s) were generated."
    )

    return {
        "product": "Sentinel Evidence Defensibility Workbench",
        "company": "Eye On Bits Pvt Ltd",
        "version": "4.0.0",
        "review_timestamp": datetime.utcnow().isoformat(),
        "organization": payload.organization,
        "industry": payload.industry,
        "evidence_type": payload.evidence_type,
        "review_objective": payload.review_objective,
        "evidence_defensibility_score": overall_score,
        "intake_coverage_score": intake_score,
        "metadata_completeness_score": metadata_score,
        "overall_rating": rating,
        "total_findings": len(findings),
        "high_risk_findings": len([f for f in findings if f["severity"] in ["Critical", "High"]]),
        "severity_distribution": severity_distribution,
        "top_risk_domains": sorted([{"domain": k, "count": v} for k, v in domain_counts.items()], key=lambda x: x["count"], reverse=True),
        "framework_coverage": sorted([{"framework": k, "count": v} for k, v in framework_counts.items()], key=lambda x: x["count"], reverse=True),
        "item_scorecards": item_scores,
        "findings": findings,
        "evidence_requests": evidence_requests,
        "recommended_next_steps": [
            "Address missing metadata first: owner, source system, reporting period, evidence date, and control reference.",
            "Use the intake gap analysis to collect missing required evidence elements by domain.",
            "Review high and critical findings with accountable evidence owners.",
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
        conn.execute(
            """
            INSERT INTO reviews (
                id, created_at, updated_at, organization, industry, evidence_type, review_objective,
                overall_rating, evidence_defensibility_score, intake_coverage_score, metadata_completeness_score,
                total_findings, payload_json, result_json, register_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                review_id,
                now,
                now,
                payload.organization,
                payload.industry,
                payload.evidence_type,
                payload.review_objective,
                result["overall_rating"],
                result["evidence_defensibility_score"],
                result["intake_coverage_score"],
                result["metadata_completeness_score"],
                result["total_findings"],
                json.dumps(payload.model_dump()),
                json.dumps(result_with_id),
                json.dumps(register),
            ),
        )
        conn.commit()

    return result_with_id

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Sentinel Evidence Defensibility Workbench",
        "version": "4.0.0",
        "database": str(DB_PATH),
        "timestamp": datetime.utcnow().isoformat()
    }

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
    result = build_analysis(payload)
    return save_review(payload, result)

@app.get("/api/reviews")
def list_reviews():
    ensure_db()
    with db() as conn:
        rows = conn.execute(
            """
            SELECT id, created_at, updated_at, organization, industry, evidence_type, overall_rating,
                   evidence_defensibility_score, intake_coverage_score, metadata_completeness_score, total_findings
            FROM reviews
            ORDER BY created_at DESC
            """
        ).fetchall()

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
        conn.execute(
            "UPDATE reviews SET updated_at = ?, result_json = ?, register_json = ? WHERE id = ?",
            (now, json.dumps(result), json.dumps(update.rows), review_id),
        )
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

def render_html_report(result: Dict[str, Any]) -> str:
    score_rows = ""
    for item in result["item_scorecards"]:
        dim_rows = "".join(
            f"<tr><td>{html.escape(d['label'])}</td><td>{d['score']}/100</td><td>{html.escape(d['rating'])}</td><td>{html.escape(', '.join(d['negative_indicators']) or 'None')}</td></tr>"
            for d in item["dimensions"]
        )
        intake = item["intake_gap_analysis"]
        profile = item["artifact_profile"]
        score_rows += f"""
        <div class='finding'>
          <h3>{html.escape(item['item_title'])}</h3>
          <p><b>Domain:</b> {html.escape(item['domain'])} | <b>Score:</b> {item['score']}/100 | <b>Rating:</b> {html.escape(item['rating'])}</p>
          <p><b>Artifact type:</b> {html.escape(profile['artifact_type'])} | <b>Metadata completeness:</b> {profile['metadata_completeness_score']}/100</p>
          <p><b>Intake coverage:</b> {intake['intake_coverage_score']}/100 | <b>Missing elements:</b> {html.escape(', '.join(intake['missing_elements']) or 'None')}</p>
          <table><tr><th>Dimension</th><th>Score</th><th>Rating</th><th>Negative Indicators</th></tr>{dim_rows}</table>
        </div>
        """

    register = result.get("remediation_register", [])
    register_rows = ""
    for row in register:
        register_rows += f"<tr><td>{html.escape(str(row.get('finding_id','')))}</td><td>{html.escape(str(row.get('severity','')))}</td><td>{html.escape(str(row.get('owner','')))}</td><td>{html.escape(str(row.get('target_date','')))}</td><td>{html.escape(str(row.get('status','')))}</td><td>{html.escape(str(row.get('management_response','')))}</td></tr>"

    finding_blocks = ""
    for f in result["findings"]:
        mapping_rows = ""
        for m in f.get("framework_mappings", []):
            mapping_rows += f"<tr><td>{html.escape(m['framework'])}</td><td>{html.escape(m['mapping_type'])}</td><td>{html.escape(m['rationale'])}</td><td>{html.escape(m['evidence_expected'])}</td></tr>"

        finding_blocks += f"""
        <div class='finding'>
          <div class='finding-head'>
            <h3>{html.escape(f["finding_id"])} — {html.escape(f["title"])}</h3>
            <span class='badge {html.escape(f["severity"].lower())}'>{html.escape(f["severity"])}</span>
          </div>
          <p><b>Risk domain:</b> {html.escape(f["risk_domain"])}</p>
          <p><b>Affected item:</b> {html.escape(f["affected_item"])}</p>
          <p><b>Severity rationale:</b> {html.escape(f["severity_rationale"])}</p>
          <p><b>Evidence gap:</b> {html.escape(f["evidence_gap"])}</p>
          <p><b>Examiner question:</b> {html.escape(f["examiner_question"])}</p>
          <p><b>Remediation:</b> {html.escape(f["remediation"])}</p>
          <h4>Framework Mapping Rationale</h4>
          <table><tr><th>Framework</th><th>Mapping Type</th><th>Rationale</th><th>Expected Evidence</th></tr>{mapping_rows}</table>
        </div>
        """

    steps = "".join([f"<li>{html.escape(x)}</li>" for x in result["recommended_next_steps"]])

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Evidence Defensibility Report</title>
<style>
body {{ font-family: Arial, sans-serif; background: #f6f8fb; color: #111827; margin: 0; padding: 32px; }}
.report {{ max-width: 1220px; margin: auto; background: white; border-radius: 18px; padding: 36px; box-shadow: 0 20px 60px rgba(15,23,42,.12); }}
.eyebrow {{ color: #1d4ed8; text-transform: uppercase; font-size: 12px; font-weight: 700; letter-spacing: .18em; }}
h1 {{ font-size: 38px; margin: 8px 0 4px; }}
.sub {{ color: #4b5563; font-size: 16px; }}
.cards {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin: 24px 0; }}
.card {{ border: 1px solid #e5e7eb; border-radius: 14px; padding: 16px; background: #f9fafb; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:22px; margin-top:6px; }}
.summary {{ border-left: 5px solid #1d4ed8; background: #eff6ff; padding: 16px; border-radius: 12px; margin: 18px 0; }}
.finding {{ border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px; margin: 16px 0; }}
.finding-head {{ display:flex; justify-content:space-between; align-items:center; gap:12px; }}
.finding h3 {{ margin:0; }}
.badge {{ border-radius:999px; padding:7px 11px; color:white; font-size:12px; font-weight:700; }}
.high {{ background:#b91c1c; }} .medium {{ background:#b45309; }} .low {{ background:#047857; }} .critical {{ background:#7f1d1d; }}
table {{ width:100%; border-collapse: collapse; margin-top:12px; font-size: 13px; }}
td, th {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; vertical-align: top; }}
.footer {{ margin-top: 28px; color: #6b7280; font-size: 12px; }}
@media print {{ body {{ background:white; padding:0; }} .report {{ box-shadow:none; }} }}
</style>
</head>
<body>
<div class='report'>
<div class='eyebrow'>Eye On Bits Pvt Ltd</div>
<h1>Sentinel Evidence Defensibility Report</h1>
<div class='sub'>Persistent review-vault output for evidence quality, intake completeness, metadata quality, findings, remediation register, and framework mapping rationale.</div>
<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(result["organization"])}</strong></div>
<div class='card'><span>Defensibility</span><strong>{result["evidence_defensibility_score"]}/100</strong></div>
<div class='card'><span>Intake</span><strong>{result["intake_coverage_score"]}/100</strong></div>
<div class='card'><span>Metadata</span><strong>{result["metadata_completeness_score"]}/100</strong></div>
<div class='card'><span>Rating</span><strong>{html.escape(result["overall_rating"])}</strong></div>
</div>
<div class='summary'>{html.escape(result["executive_summary"])}</div>
<h2>Remediation Register</h2>
<table><tr><th>Finding</th><th>Severity</th><th>Owner</th><th>Target Date</th><th>Status</th><th>Management Response</th></tr>{register_rows}</table>
<h2>Scorecards and Intake Diagnostics</h2>
{score_rows}
<h2>Recommended Next Steps</h2>
<ol>{steps}</ol>
<h2>Findings</h2>
{finding_blocks}
<div class='footer'>Generated by Sentinel Evidence Defensibility Workbench v4.0. This output supports assurance review and does not replace qualified professional judgment.</div>
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
    result = get_review(review_id)
    return render_html_report(result)


def _portfolio_snapshot_from_reviews(rows: List[sqlite3.Row]) -> Dict[str, Any]:
    reviews = [dict(row) for row in rows]
    total_reviews = len(reviews)
    avg_defensibility = round(sum((r.get("evidence_defensibility_score") or 0) for r in reviews) / total_reviews) if total_reviews else 0
    avg_intake = round(sum((r.get("intake_coverage_score") or 0) for r in reviews) / total_reviews) if total_reviews else 0
    avg_metadata = round(sum((r.get("metadata_completeness_score") or 0) for r in reviews) / total_reviews) if total_reviews else 0
    total_findings = sum((r.get("total_findings") or 0) for r in reviews)

    rating_distribution: Dict[str, int] = {}
    evidence_type_distribution: Dict[str, int] = {}

    for r in reviews:
        rating = r.get("overall_rating") or "Unknown"
        evidence_type = r.get("evidence_type") or "Unknown"
        rating_distribution[rating] = rating_distribution.get(rating, 0) + 1
        evidence_type_distribution[evidence_type] = evidence_type_distribution.get(evidence_type, 0) + 1

    open_register_items = 0
    in_progress_register_items = 0
    closed_register_items = 0
    high_or_critical_items = 0
    domain_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}
    severity_counts: Dict[str, int] = {}

    with db() as conn:
        full_rows = conn.execute("SELECT register_json, result_json FROM reviews").fetchall()

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
        "reviews": reviews
    }

@app.get("/api/portfolio")
def portfolio_dashboard():
    ensure_db()
    with db() as conn:
        rows = conn.execute(
            """
            SELECT id, created_at, updated_at, organization, industry, evidence_type, overall_rating,
                   evidence_defensibility_score, intake_coverage_score, metadata_completeness_score, total_findings
            FROM reviews
            ORDER BY created_at DESC
            """
        ).fetchall()

    return _portfolio_snapshot_from_reviews(rows)

@app.get("/api/portfolio/report-html", response_class=HTMLResponse)
def portfolio_report_html():
    snapshot = portfolio_dashboard()

    review_rows = ""
    for r in snapshot["reviews"]:
        review_rows += f"""
        <tr>
          <td>{html.escape(str(r.get("organization", "")))}</td>
          <td>{html.escape(str(r.get("evidence_type", "")))}</td>
          <td>{html.escape(str(r.get("overall_rating", "")))}</td>
          <td>{r.get("evidence_defensibility_score", "")}/100</td>
          <td>{r.get("intake_coverage_score", "")}/100</td>
          <td>{r.get("metadata_completeness_score", "")}/100</td>
          <td>{r.get("total_findings", "")}</td>
          <td>{html.escape(str(r.get("created_at", "")))}</td>
        </tr>
        """

    domain_rows = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
        for k, v in sorted(snapshot["risk_domain_distribution"].items(), key=lambda x: x[1], reverse=True)
    )
    severity_rows = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
        for k, v in sorted(snapshot["severity_distribution"].items(), key=lambda x: x[1], reverse=True)
    )
    status_rows = "".join(
        f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
        for k, v in sorted(snapshot["register_status_distribution"].items(), key=lambda x: x[1], reverse=True)
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Sentinel Portfolio Command Center Report</title>
<style>
body {{ font-family: Arial, sans-serif; background:#f5f7fb; color:#111827; margin:0; padding:32px; }}
.report {{ max-width:1280px; margin:auto; background:white; border-radius:20px; padding:36px; box-shadow:0 20px 60px rgba(15,23,42,.12); }}
.eyebrow {{ color:#1d4ed8; text-transform:uppercase; letter-spacing:.18em; font-size:12px; font-weight:800; }}
h1 {{ margin:8px 0; font-size:38px; }}
.sub {{ color:#4b5563; }}
.cards {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin:24px 0; }}
.card {{ background:#f9fafb; border:1px solid #e5e7eb; border-radius:14px; padding:16px; }}
.card span {{ display:block; color:#6b7280; font-size:12px; text-transform:uppercase; }}
.card strong {{ display:block; font-size:23px; margin-top:6px; }}
.grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
.panel {{ border:1px solid #e5e7eb; border-radius:16px; padding:18px; margin:16px 0; }}
table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }}
th, td {{ border-bottom:1px solid #e5e7eb; padding:10px; text-align:left; vertical-align:top; }}
.summary {{ border-left:5px solid #1d4ed8; background:#eff6ff; padding:16px; border-radius:12px; margin:18px 0; }}
.footer {{ color:#6b7280; font-size:12px; margin-top:24px; }}
@media print {{ body {{ background:white; padding:0; }} .report {{ box-shadow:none; }} }}
</style>
</head>
<body>
<div class='report'>
<div class='eyebrow'>Eye On Bits Pvt Ltd · Sentinel v4.0</div>
<h1>Portfolio Command Center Report</h1>
<p class='sub'>Executive snapshot across saved evidence defensibility reviews, remediation register status, severity distribution, and recurring risk domains.</p>
<div class='cards'>
<div class='card'><span>Total Reviews</span><strong>{snapshot["total_reviews"]}</strong></div>
<div class='card'><span>Avg Defensibility</span><strong>{snapshot["average_defensibility_score"]}/100</strong></div>
<div class='card'><span>Avg Intake</span><strong>{snapshot["average_intake_score"]}/100</strong></div>
<div class='card'><span>Avg Metadata</span><strong>{snapshot["average_metadata_score"]}/100</strong></div>
<div class='card'><span>Open Items</span><strong>{snapshot["open_register_items"]}</strong></div>
</div>
<div class='summary'>Sentinel identified {snapshot["total_findings"]} total findings across {snapshot["total_reviews"]} saved review(s), including {snapshot["high_or_critical_findings"]} high or critical finding(s). Current remediation status includes {snapshot["open_register_items"]} open, {snapshot["in_progress_register_items"]} in progress, and {snapshot["closed_register_items"]} closed item(s).</div>
<div class='grid'>
<div class='panel'><h2>Risk Domains</h2><table><tr><th>Domain</th><th>Count</th></tr>{domain_rows}</table></div>
<div class='panel'><h2>Severity</h2><table><tr><th>Severity</th><th>Count</th></tr>{severity_rows}</table></div>
<div class='panel'><h2>Register Status</h2><table><tr><th>Status</th><th>Count</th></tr>{status_rows}</table></div>
</div>
<h2>Saved Reviews</h2>
<table><tr><th>Organization</th><th>Evidence Type</th><th>Rating</th><th>Defensibility</th><th>Intake</th><th>Metadata</th><th>Findings</th><th>Created</th></tr>{review_rows}</table>
<div class='footer'>Generated by Sentinel Evidence Defensibility Workbench v4.0. This report is a local prototype output for professional assurance workflow demonstration.</div>
</div>
</body>
</html>"""

@app.post("/api/demo/seed")
def seed_demo_reviews():
    examples = [
        {
            "organization": "Sample Tier-1 Bank",
            "industry": "BFSI / Regulated Banking",
            "evidence_type": "IT Metrics Defensibility Review",
            "review_objective": "Assess denominator consistency, source lineage, calculation logic, and committee reporting tie-out.",
            "items": [
                {
                    "title": "Q4 Phishing Metric Evidence",
                    "content": "The ITSC deck reported 150 delivered emails. KnowBe4 source export shows denominator changed to 152. Screenshot-only evidence was retained. No reviewer approval or reconciliation is attached.",
                    "source_system": "KnowBe4 / ITSC Deck",
                    "owner": "IT GRC",
                    "reporting_period": "Q4",
                    "artifact_type": "Metric Evidence"
                }
            ]
        },
        {
            "organization": "Sample Financial Institution",
            "industry": "BFSI / Vendor Risk",
            "evidence_type": "Vendor and Privacy Evidence Review",
            "review_objective": "Assess SOC 2 reliance, CUEC analysis, data-flow evidence, retention, and customer information handling.",
            "items": [
                {
                    "title": "Vendor SOC 2 Evidence",
                    "content": "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, bridge letter, subservice organization review, DPA, or CUEC analysis.",
                    "source_system": "Vendor Portal",
                    "owner": "TPRM",
                    "reporting_period": "Annual Review",
                    "artifact_type": "SOC 2 / Vendor Evidence"
                }
            ]
        },
        {
            "organization": "Sample Enterprise Technology Group",
            "industry": "Technology / AI Governance",
            "evidence_type": "SDLC and AI Governance Review",
            "review_objective": "Assess release governance, AI approval, security gates, monitoring, and production readiness evidence.",
            "items": [
                {
                    "title": "AI-Enabled Release Evidence",
                    "content": "Release notes mention AI assistant functionality and production rollout. No AI inventory entry, risk tier, approval record, security gate, change record, monitoring plan, or incident escalation logic.",
                    "source_system": "DevOps Release Tracker",
                    "owner": "Application Owner",
                    "reporting_period": "Release 2026.05",
                    "artifact_type": "AI Release Evidence"
                }
            ]
        }
    ]

    saved = []
    for example in examples:
        payload = AnalyzeRequest(**example)
        result = build_analysis(payload)
        saved.append(save_review(payload, result))

    return {"status": "seeded", "reviews_created": len(saved), "review_ids": [x["review_id"] for x in saved]}
