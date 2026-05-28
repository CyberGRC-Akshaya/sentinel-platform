from pydantic import BaseModel
from typing import Any, Dict, List, Optional

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

