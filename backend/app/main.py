from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
import html

app = FastAPI(
    title="Sentinel Evidence Defensibility Workbench",
    description="Professional assurance workbench for evidence defensibility review across IT metrics, vendor risk, privacy, SDLC, IAM, and AI governance.",
    version="2.0.0"
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
            "rationale": "Management reporting and control metrics should be supported by traceable source data, defined calculation logic, reporting-period alignment, and review evidence.",
            "evidence_expected": "Metric definition, source export, numerator/denominator logic, reconciliation, reviewer approval, and committee/reporting tie-out."
        },
        {
            "framework": "GLBA 501(b) Program Governance Relevance",
            "mapping_type": "Program oversight relevance",
            "rationale": "Security program oversight depends on reliable governance reporting and defensible evidence over risk and control performance.",
            "evidence_expected": "Validated security metrics, governance reporting package, management review evidence, and remediation tracking."
        },
        {
            "framework": "NIST CSF Govern",
            "mapping_type": "Control framework relevance",
            "rationale": "Governance outcomes require risk-informed oversight, measurement, accountability, and evidence-based decision-making.",
            "evidence_expected": "Risk reporting, accountable owner review, control monitoring evidence, and escalation records."
        }
    ],
    "Third-Party Risk": [
        {
            "framework": "AICPA SOC 2",
            "mapping_type": "Assurance reliance relevance",
            "rationale": "SOC 2 reliance requires understanding scope, exceptions, subservice organizations, system boundaries, and complementary user entity controls.",
            "evidence_expected": "SOC 2 report, bridge letter if applicable, CUEC analysis, subservice review, internal owner mapping, and residual risk conclusion."
        },
        {
            "framework": "FFIEC Outsourcing / Third-Party Risk Expectations",
            "mapping_type": "Third-party oversight relevance",
            "rationale": "Outsourced technology risk should be evaluated through due diligence, contractual obligations, monitoring, and risk-based oversight.",
            "evidence_expected": "Due diligence evidence, contract/security addendum, vendor risk assessment, monitoring artifacts, and issue tracking."
        }
    ],
    "Privacy / Data Protection": [
        {
            "framework": "GLBA Customer Information Safeguards Relevance",
            "mapping_type": "Data protection relevance",
            "rationale": "Customer information handling should be supported by safeguards, access boundaries, retention controls, and third-party oversight where applicable.",
            "evidence_expected": "Data-flow diagram, processing purpose, access list, retention/destruction evidence, vendor transfer evidence, and privacy/security obligations."
        },
        {
            "framework": "NIST Privacy Framework / ISO 27701 Relevance",
            "mapping_type": "Privacy governance relevance",
            "rationale": "Privacy risk management requires understanding data actions, processing responsibilities, minimization, retention, and control accountability.",
            "evidence_expected": "Processing inventory, privacy impact review, data minimization rationale, retention controls, and processor/controller obligations."
        }
    ],
    "SDLC / Change / DevSecOps": [
        {
            "framework": "FFIEC Development, Acquisition, and Maintenance",
            "mapping_type": "Technology governance relevance",
            "rationale": "System changes and development activities should be governed, tested, approved, risk-assessed, and controlled before production movement.",
            "evidence_expected": "Change record, release approval, security testing results, exception/risk acceptance, deployment record, and rollback evidence."
        },
        {
            "framework": "NIST SSDF / Secure SDLC Good Practice",
            "mapping_type": "Secure development relevance",
            "rationale": "Secure software development should evidence secure design, testing, vulnerability handling, and release integrity.",
            "evidence_expected": "SAST/DAST/pentest evidence, vulnerability disposition, code/release review, approval gate evidence, and production readiness confirmation."
        }
    ],
    "AI Governance": [
        {
            "framework": "NIST AI RMF",
            "mapping_type": "AI risk governance relevance",
            "rationale": "AI systems should be governed, mapped, measured, and managed based on intended use, risk, impact, and monitoring obligations.",
            "evidence_expected": "AI inventory, use case owner, risk tier/classification, data review, monitoring plan, approval record, and incident escalation criteria."
        },
        {
            "framework": "ISO/IEC 42001",
            "mapping_type": "AI management system relevance",
            "rationale": "AI governance should be supported by accountable management system practices, documented responsibilities, risk treatment, and monitoring evidence.",
            "evidence_expected": "AI management roles, policy/standard evidence, risk treatment records, use case approvals, and monitoring evidence."
        }
    ],
    "Identity & Access": [
        {
            "framework": "FFIEC Authentication / Access Governance Expectations",
            "mapping_type": "Access control relevance",
            "rationale": "Access and authentication controls should be risk-based, approved, reviewed, monitored, and supported by exception handling evidence.",
            "evidence_expected": "Access request and approval, authentication control coverage, MFA/risk decision evidence, periodic review, exception register, and revocation evidence."
        },
        {
            "framework": "ISO 27001 Access Control",
            "mapping_type": "Control framework relevance",
            "rationale": "Identity lifecycle and access controls require authorization, review, revocation, and privileged access governance.",
            "evidence_expected": "Joiner/mover/leaver records, access certification, privileged access review, and remediation closure evidence."
        }
    ],
    "General Evidence Defensibility": [
        {
            "framework": "Audit Evidence Discipline",
            "mapping_type": "Professional assurance relevance",
            "rationale": "Evidence should be sufficient, reliable, relevant, retained, reviewed, and clearly tied to the claim being supported.",
            "evidence_expected": "Evidence objective, source, owner, date, review trail, conclusion, and linkage to control or risk statement."
        }
    ]
}

DIMENSIONS = [
    {
        "key": "source_lineage",
        "label": "Source Lineage",
        "weight": 18,
        "positive": ["source export", "system export", "source-of-record", "source of record", "query", "extract", "timestamp", "system generated"],
        "negative": ["screenshot-only", "screenshot only", "manual", "email screenshot", "corrected later"]
    },
    {
        "key": "completeness",
        "label": "Completeness",
        "weight": 16,
        "positive": ["population", "complete", "full extract", "all records", "reconciliation", "tie-out"],
        "negative": ["partial", "sample only", "not included", "missing", "not available", "does not include"]
    },
    {
        "key": "calculation_integrity",
        "label": "Calculation Integrity",
        "weight": 16,
        "positive": ["numerator", "denominator", "formula", "calculation", "logic", "recalculation", "validated"],
        "negative": ["changed to", "mismatch", "inconsistent", "corrected later", "cumulative", "unclear"]
    },
    {
        "key": "review_approval",
        "label": "Review & Approval Evidence",
        "weight": 14,
        "positive": ["approved", "reviewed", "sign-off", "attested", "owner approval", "committee approved"],
        "negative": ["no approval", "not approved", "no review", "review not shown", "owner stated"]
    },
    {
        "key": "period_alignment",
        "label": "Reporting Period Alignment",
        "weight": 12,
        "positive": ["q1", "q2", "q3", "q4", "monthly", "quarterly", "annual", "reporting period", "as of"],
        "negative": ["year-to-date", "ytd", "cumulative", "prior period", "unclear period"]
    },
    {
        "key": "governance_traceability",
        "label": "Governance Traceability",
        "weight": 14,
        "positive": ["policy", "standard", "control", "risk acceptance", "exception", "issue", "ticket", "change record"],
        "negative": ["no ticket", "no change record", "no exception", "no risk acceptance", "not documented"]
    },
    {
        "key": "data_handling",
        "label": "Data Handling & Privacy Boundary",
        "weight": 10,
        "positive": ["data flow", "retention", "pii", "npi", "customer data", "encryption", "access boundary", "dpa"],
        "negative": ["no data flow", "retention not", "unknown retention", "no dpa", "not documented"]
    }
]

DOMAIN_KEYWORDS = [
    ("AI Governance", [" ai ", "genai", "model", "prompt", "copilot", "assistant", "machine learning", "inventory", "risk tier"]),
    ("Identity & Access", ["iam", "access", "authentication", "mfa", "privileged", "password", "user review", "entitlement"]),
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
    metadata: Optional[Dict[str, Any]] = {}

class AnalyzeRequest(BaseModel):
    organization: str
    industry: str
    evidence_type: str
    review_objective: str
    items: List[EvidenceItem]

def normalize_text(item: EvidenceItem) -> str:
    return f" {item.title} {item.content} {item.source_system or ''} {item.owner or ''} {item.reporting_period or ''} ".lower()

def detect_domain(text: str) -> str:
    for domain, keywords in DOMAIN_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return domain
    return "General Evidence Defensibility"

def dimension_score(text: str, dimension: Dict[str, Any]) -> Dict[str, Any]:
    base = 65
    positive_hits = [p for p in dimension["positive"] if p in text]
    negative_hits = [n for n in dimension["negative"] if n in text]

    score = base + (len(positive_hits) * 8) - (len(negative_hits) * 12)
    score = max(0, min(100, score))

    if score >= 80:
        rating = "Strong"
    elif score >= 60:
        rating = "Moderate"
    elif score >= 40:
        rating = "Weak"
    else:
        rating = "Deficient"

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
    dimension_results = [dimension_score(text, d) for d in DIMENSIONS]
    weighted_total = sum((d["score"] * d["weight"]) for d in dimension_results)
    total_weight = sum(d["weight"] for d in dimension_results)
    score = round(weighted_total / total_weight)

    if score >= 85:
        rating = "Strong"
    elif score >= 70:
        rating = "Moderate"
    elif score >= 50:
        rating = "Weak"
    else:
        rating = "Critical Attention Required"

    return {
        "item_title": item.title,
        "domain": detect_domain(text),
        "score": score,
        "rating": rating,
        "dimensions": dimension_results
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

    issue_title = f"{dimension['label']} Defensibility Gap"

    negative = ", ".join(dimension.get("negative_indicators", [])) or "insufficient positive evidence indicators"
    positive = ", ".join(dimension.get("positive_indicators", [])) or "limited traceable evidence"

    severity_rationale = (
        f"{dimension['label']} scored {dimension['score']}/100 and is rated {dimension['rating']} "
        f"based on negative indicators ({negative}) and positive indicators ({positive})."
    )

    evidence_gap = f"The submitted evidence does not sufficiently demonstrate {dimension['label'].lower()} for the claim being reviewed."

    question = f"What evidence proves {dimension['label'].lower()} for '{item.title}', and who reviewed or approved that evidence?"

    request = {
        "request_id": f"REQ-{idx:03d}",
        "evidence_needed": f"Provide evidence supporting {dimension['label'].lower()} for {item.title}.",
        "preferred_artifacts": [],
        "owner": item.owner or "Evidence Owner",
        "priority": severity,
        "status": "Open"
    }

    preferred = {
        "source_lineage": ["source-of-record extract", "query/filter criteria", "timestamped export", "extract owner evidence"],
        "completeness": ["population report", "reconciliation", "scope definition", "sample basis if sampling was used"],
        "calculation_integrity": ["metric definition", "formula", "numerator/denominator support", "independent recalculation"],
        "review_approval": ["review notes", "approval record", "control owner sign-off", "committee approval where applicable"],
        "period_alignment": ["reporting calendar", "as-of date evidence", "period-specific extract", "committee reporting tie-out"],
        "governance_traceability": ["ticket/change record", "risk acceptance", "exception approval", "issue/remediation tracker"],
        "data_handling": ["data-flow diagram", "retention evidence", "access boundary evidence", "contractual/privacy obligation"]
    }

    request["preferred_artifacts"] = preferred.get(dimension["key"], ["supporting evidence package"])

    return {
        "finding_id": f"SEN-{idx:03d}",
        "title": issue_title,
        "severity": severity,
        "severity_rationale": severity_rationale,
        "risk_domain": domain,
        "affected_item": item.title,
        "dimension": dimension["label"],
        "issue": f"{dimension['label']} is not sufficiently evidenced for this review item.",
        "evidence_gap": evidence_gap,
        "examiner_question": question,
        "remediation": f"Provide traceable evidence and management review support for {dimension['label'].lower()}.",
        "framework_relevance": [m["framework"] for m in framework_mappings_for(domain)],
        "framework_mappings": framework_mappings_for(domain),
        "evidence_request": request,
        "management_response": "",
        "status": "Open"
    }

def build_analysis(payload: AnalyzeRequest) -> Dict[str, Any]:
    item_scores = [score_item(item) for item in payload.items]
    findings: List[Dict[str, Any]] = []
    request_counter = 1

    for item, item_score in zip(payload.items, item_scores):
        weak_dimensions = [
            d for d in item_score["dimensions"]
            if d["score"] < 70 or d["negative_indicators"]
        ]

        weak_dimensions = sorted(weak_dimensions, key=lambda d: d["score"])[:4]

        for dim in weak_dimensions:
            findings.append(build_finding(item, item_score, dim, request_counter))
            request_counter += 1

    if not findings:
        domain = item_scores[0]["domain"] if item_scores else "General Evidence Defensibility"
        findings.append({
            "finding_id": "SEN-001",
            "title": "No Immediate High-Risk Evidence Gap Detected",
            "severity": "Low",
            "severity_rationale": "No major rule-based issue was detected. Professional review is still required before relying on the evidence package.",
            "risk_domain": domain,
            "affected_item": "Overall Evidence Package",
            "dimension": "General Review",
            "issue": "No immediate high-risk issue detected by deterministic review.",
            "evidence_gap": "Human review should confirm completeness, reliability, and relevance.",
            "examiner_question": "Can management demonstrate complete source lineage and review approval for this package?",
            "remediation": "Retain full source evidence, review notes, and approval trail.",
            "framework_relevance": [m["framework"] for m in framework_mappings_for(domain)],
            "framework_mappings": framework_mappings_for(domain),
            "evidence_request": {
                "request_id": "REQ-001",
                "evidence_needed": "Retain source evidence, review notes, and approval trail.",
                "preferred_artifacts": ["source extract", "review notes", "approval record"],
                "owner": "Evidence Owner",
                "priority": "Low",
                "status": "Open"
            },
            "management_response": "",
            "status": "Open"
        })

    overall_score = round(sum(i["score"] for i in item_scores) / len(item_scores)) if item_scores else 0

    if overall_score >= 85:
        rating = "Strong"
    elif overall_score >= 70:
        rating = "Moderate"
    elif overall_score >= 50:
        rating = "Weak"
    else:
        rating = "Critical Attention Required"

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
        f"Sentinel reviewed {len(payload.items)} evidence item(s) across {len(set(i['domain'] for i in item_scores))} risk domain(s). "
        f"The package is rated '{rating}' with an evidence defensibility score of {overall_score}/100. "
        f"{len(findings)} finding(s) and {len(evidence_requests)} evidence request(s) were generated for management follow-up."
    )

    return {
        "product": "Sentinel Evidence Defensibility Workbench",
        "company": "Eye On Bits Pvt Ltd",
        "version": "2.0.0",
        "review_timestamp": datetime.utcnow().isoformat(),
        "organization": payload.organization,
        "industry": payload.industry,
        "evidence_type": payload.evidence_type,
        "review_objective": payload.review_objective,
        "evidence_defensibility_score": overall_score,
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
            "Review high and critical findings with accountable evidence owners.",
            "Use the evidence request list to collect missing source, review, approval, and reconciliation artifacts.",
            "Update the finding register with owner, target date, management response, and closure evidence.",
            "Use framework mapping rationale for audit, 2LOD, or committee-ready explanation.",
            "Re-run Sentinel after remediation evidence is collected."
        ],
        "executive_summary": executive_summary
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Sentinel Evidence Defensibility Workbench",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/framework-library")
def framework_library():
    return FRAMEWORK_LIBRARY

@app.get("/api/scoring-dimensions")
def scoring_dimensions():
    return DIMENSIONS

@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    return build_analysis(payload)

@app.post("/api/report-html", response_class=HTMLResponse)
def report_html(payload: AnalyzeRequest):
    result = build_analysis(payload)

    score_rows = ""
    for item in result["item_scorecards"]:
        dim_rows = "".join(
            f"<tr><td>{html.escape(d['label'])}</td><td>{d['score']}/100</td><td>{html.escape(d['rating'])}</td><td>{html.escape(', '.join(d['negative_indicators']) or 'None')}</td></tr>"
            for d in item["dimensions"]
        )
        score_rows += f"""
        <div class='finding'>
          <h3>{html.escape(item['item_title'])}</h3>
          <p><b>Domain:</b> {html.escape(item['domain'])} | <b>Score:</b> {item['score']}/100 | <b>Rating:</b> {html.escape(item['rating'])}</p>
          <table><tr><th>Dimension</th><th>Score</th><th>Rating</th><th>Negative Indicators</th></tr>{dim_rows}</table>
        </div>
        """

    finding_blocks = ""
    for f in result["findings"]:
        mapping_rows = ""
        for m in f.get("framework_mappings", []):
            mapping_rows += f"<tr><td>{html.escape(m['framework'])}</td><td>{html.escape(m['mapping_type'])}</td><td>{html.escape(m['rationale'])}</td><td>{html.escape(m['evidence_expected'])}</td></tr>"

        req = f["evidence_request"]
        artifacts = ", ".join(req.get("preferred_artifacts", []))

        finding_blocks += f"""
        <div class='finding'>
          <div class='finding-head'>
            <h3>{html.escape(f["finding_id"])} — {html.escape(f["title"])}</h3>
            <span class='badge {html.escape(f["severity"].lower())}'>{html.escape(f["severity"])}</span>
          </div>
          <p><b>Risk domain:</b> {html.escape(f["risk_domain"])}</p>
          <p><b>Affected item:</b> {html.escape(f["affected_item"])}</p>
          <p><b>Dimension:</b> {html.escape(f["dimension"])}</p>
          <p><b>Issue:</b> {html.escape(f["issue"])}</p>
          <p><b>Severity rationale:</b> {html.escape(f["severity_rationale"])}</p>
          <p><b>Evidence gap:</b> {html.escape(f["evidence_gap"])}</p>
          <p><b>Examiner question:</b> {html.escape(f["examiner_question"])}</p>
          <p><b>Remediation:</b> {html.escape(f["remediation"])}</p>
          <h4>Evidence Request</h4>
          <p><b>{html.escape(req["request_id"])}:</b> {html.escape(req["evidence_needed"])}</p>
          <p><b>Preferred artifacts:</b> {html.escape(artifacts)}</p>
          <h4>Framework Mapping Rationale</h4>
          <table><tr><th>Framework</th><th>Mapping Type</th><th>Rationale</th><th>Expected Evidence</th></tr>{mapping_rows}</table>
        </div>
        """

    requests = ""
    for req in result["evidence_requests"]:
        requests += f"<tr><td>{html.escape(req['request_id'])}</td><td>{html.escape(req['priority'])}</td><td>{html.escape(req['owner'])}</td><td>{html.escape(req['evidence_needed'])}</td><td>{html.escape(', '.join(req.get('preferred_artifacts', [])))}</td><td>{html.escape(req['status'])}</td></tr>"

    domain_rows = "".join([f"<tr><td>{html.escape(x['domain'])}</td><td>{x['count']}</td></tr>" for x in result["top_risk_domains"]])
    framework_rows = "".join([f"<tr><td>{html.escape(x['framework'])}</td><td>{x['count']}</td></tr>" for x in result["framework_coverage"]])
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
.cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 24px 0; }}
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
<div class='sub'>Professional assurance workbench output for evidence quality, scoring, findings, evidence requests, and framework mapping rationale.</div>
<div class='cards'>
<div class='card'><span>Organization</span><strong>{html.escape(result["organization"])}</strong></div>
<div class='card'><span>Evidence Type</span><strong>{html.escape(result["evidence_type"])}</strong></div>
<div class='card'><span>Score</span><strong>{result["evidence_defensibility_score"]}/100</strong></div>
<div class='card'><span>Rating</span><strong>{html.escape(result["overall_rating"])}</strong></div>
</div>
<div class='summary'>{html.escape(result["executive_summary"])}</div>
<h2>Scorecards</h2>
{score_rows}
<h2>Evidence Request List</h2>
<table><tr><th>Request ID</th><th>Priority</th><th>Owner</th><th>Evidence Needed</th><th>Preferred Artifacts</th><th>Status</th></tr>{requests}</table>
<h2>Top Risk Domains</h2>
<table><tr><th>Domain</th><th>Finding Count</th></tr>{domain_rows}</table>
<h2>Framework Coverage</h2>
<table><tr><th>Framework</th><th>Mapped Findings</th></tr>{framework_rows}</table>
<h2>Recommended Next Steps</h2>
<ol>{steps}</ol>
<h2>Findings</h2>
{finding_blocks}
<div class='footer'>Generated by Sentinel Evidence Defensibility Workbench v2.0. This output supports assurance review and does not replace qualified professional judgment.</div>
</div>
</body>
</html>"""
