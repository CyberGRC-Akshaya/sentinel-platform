"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const cases: Record<string, any> = {
  "IT Metrics Examiner": {
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
      }
    ]
  },
  "Vendor & Privacy Examiner": {
    organization: "Sample Financial Institution",
    industry: "BFSI / Vendor Risk",
    evidence_type: "TPRM and Privacy Evidence Review",
    review_objective: "Challenge vendor assurance package for SOC 2 reliance, customer data handling, CUECs, retention, and data-flow evidence.",
    items: [
      {
        title: "Vendor SOC 2 Evidence",
        content: "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, or CUEC analysis.",
        source_system: "Vendor Portal",
        owner: "TPRM",
        reporting_period: "Annual Review"
      }
    ]
  },
  "SDLC & AI Governance Examiner": {
    organization: "Sample Enterprise Technology Group",
    industry: "Technology / AI Governance",
    evidence_type: "SDLC and AI Governance Evidence Review",
    review_objective: "Validate release governance, AI approval, security gates, and production-readiness evidence.",
    items: [
      {
        title: "AI-Enabled Release Evidence",
        content: "Release notes mention AI assistant functionality and production rollout. Evidence includes release summary but no AI inventory entry, risk tier, approval record, security gate, change record, or monitoring plan.",
        source_system: "DevOps Release Tracker",
        owner: "Application Owner",
        reporting_period: "Release 2026.05"
      }
    ]
  },
  "IAM Evidence Examiner": {
    organization: "Sample Bank IAM Program",
    industry: "BFSI / Identity and Access",
    evidence_type: "IAM and Authentication Evidence Review",
    review_objective: "Validate access governance, authentication coverage, approval, review, and exception handling evidence.",
    items: [
      {
        title: "Customer Access and MFA Evidence",
        content: "IAM evidence references customer access, authentication, MFA, and access review activity. Evidence does not show full approval trail, risk-based exception handling, or remediation tracking.",
        source_system: "IAM Review Tracker",
        owner: "IAM Governance",
        reporting_period: "Quarterly Review"
      }
    ]
  }
};

function defaultIntakePayload() {
  return {
    organization: "Imported Evidence Package",
    industry: "Regulated Enterprise",
    evidence_type: "Uploaded Evidence Intake Review",
    review_objective: "Challenge uploaded evidence for assurance readiness, evidence lineage, governance defensibility, and examiner-style gaps.",
    items: []
  };
}

export default function Home() {
  const [selectedCase, setSelectedCase] = useState("IT Metrics Examiner");
  const [input, setInput] = useState(JSON.stringify(cases["IT Metrics Examiner"], null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem("sentinel-review-history");
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch {
        setHistory([]);
      }
    }
  }, []);

  function saveHistory(entry: any) {
    const next = [entry, ...history].slice(0, 10);
    setHistory(next);
    localStorage.setItem("sentinel-review-history", JSON.stringify(next));
  }

  function loadCase(name: string) {
    setSelectedCase(name);
    setInput(JSON.stringify(cases[name], null, 2));
    setResult(null);
    setError("");
  }

  function buildTextPayload(fileName: string, text: string) {
    const payload = defaultIntakePayload();
    payload.items = [
      {
        title: fileName,
        content: text.slice(0, 25000),
        source_system: "Uploaded File",
        owner: "Evidence Submitter",
        reporting_period: "Uploaded Review"
      }
    ];
    return payload;
  }

  function parseCsvToPayload(fileName: string, text: string) {
    const lines = text.split(/\r?\n/).filter(Boolean);
    const payload = defaultIntakePayload();
    payload.evidence_type = "Uploaded CSV Evidence Intake Review";

    if (lines.length === 0) return payload;

    const headers = lines[0].split(",").map((h) => h.trim().replace(/^"|"$/g, ""));
    const rows = lines.slice(1).slice(0, 25);

    payload.items = rows.map((line, index) => {
      const cols = line.split(",").map((c) => c.trim().replace(/^"|"$/g, ""));
      const obj: Record<string, string> = {};
      headers.forEach((h, i) => {
        obj[h || `Column_${i + 1}`] = cols[i] || "";
      });

      return {
        title: obj.title || obj.Title || obj.name || obj.Name || `CSV Evidence Row ${index + 1}`,
        content: JSON.stringify(obj),
        source_system: obj.source_system || obj.Source_System || obj.Source || "Uploaded CSV",
        owner: obj.owner || obj.Owner || "Evidence Submitter",
        reporting_period: obj.reporting_period || obj.Reporting_Period || "Uploaded Review"
      };
    });

    return payload;
  }

  async function handleFileUpload(event: any) {
    setError("");
    const file = event.target.files?.[0];
    if (!file) return;

    const text = await file.text();

    try {
      if (file.name.toLowerCase().endsWith(".json")) {
        const parsed = JSON.parse(text);

        if (parsed.organization && parsed.items) {
          setInput(JSON.stringify(parsed, null, 2));
        } else if (Array.isArray(parsed)) {
          const payload = defaultIntakePayload();
          payload.items = parsed.map((item: any, index: number) => ({
            title: item.title || item.name || `JSON Evidence Item ${index + 1}`,
            content: typeof item === "string" ? item : JSON.stringify(item),
            source_system: item.source_system || item.source || "Uploaded JSON",
            owner: item.owner || "Evidence Submitter",
            reporting_period: item.reporting_period || "Uploaded Review"
          }));
          setInput(JSON.stringify(payload, null, 2));
        } else {
          setInput(JSON.stringify(buildTextPayload(file.name, JSON.stringify(parsed)), null, 2));
        }
      } else if (file.name.toLowerCase().endsWith(".csv")) {
        setInput(JSON.stringify(parseCsvToPayload(file.name, text), null, 2));
      } else {
        setInput(JSON.stringify(buildTextPayload(file.name, text), null, 2));
      }

      setSelectedCase("Uploaded Evidence");
      setResult(null);
    } catch (err: any) {
      setError("Could not parse uploaded file: " + err.message);
    }
  }

  async function analyze() {
    setError("");
    setResult(null);
    try {
      const payload = JSON.parse(input);
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error("Backend returned error: " + response.status);
      const data = await response.json();
      setResult(data);
      saveHistory({
        timestamp: new Date().toISOString(),
        organization: data.organization,
        evidence_type: data.evidence_type,
        rating: data.overall_rating,
        score: data.assurance_score,
        findings: data.total_findings
      });
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    }
  }

  function csvEscape(value: any) {
    const text = String(value ?? "");
    return `"${text.replace(/"/g, '""')}"`;
  }

  function downloadJson() {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-examiner-report.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadFindingRegisterCsv() {
    if (!result) return;

    const headers = [
      "Finding_ID",
      "Severity",
      "Risk_Domain",
      "Affected_Item",
      "Issue",
      "Evidence_Gap",
      "Examiner_Question",
      "Remediation",
      "Framework_Relevance",
      "Framework_Rationale",
      "Expected_Evidence",
      "Owner",
      "Target_Date",
      "Status",
      "Management_Response"
    ];

    const rows = result.findings.map((finding: any, index: number) => [
      `SEN-${String(index + 1).padStart(3, "0")}`,
      finding.severity,
      finding.risk_domain,
      finding.affected_item,
      finding.issue,
      finding.evidence_gap,
      finding.examiner_question,
      finding.remediation,
      (finding.framework_relevance || []).join("; "),
      (finding.framework_mappings || []).map((m: any) => `${m.framework}: ${m.rationale}`).join(" | "),
      (finding.framework_mappings || []).map((m: any) => `${m.framework}: ${m.evidence_expected}`).join(" | "),
      "",
      "",
      "Open",
      ""
    ]);

    const csv = [headers, ...rows].map((row) => row.map(csvEscape).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-finding-register.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function downloadHtmlReport() {
    try {
      const payload = JSON.parse(input);
      const response = await fetch(`${API_BASE}/api/report-html`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      const reportHtml = await response.text();
      const blob = new Blob([reportHtml], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "sentinel-examiner-report.html";
      a.click();
      URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || "Could not generate HTML report.");
    }
  }

  async function copySummary() {
    if (!result) return;
    await navigator.clipboard.writeText(result.executive_summary);
    alert("Executive summary copied.");
  }

  function clearHistory() {
    setHistory([]);
    localStorage.removeItem("sentinel-review-history");
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Eye On Bits Pvt Ltd</p>
          <h1>Sentinel Assurance Platform</h1>
          <p className="subtitle">AI-native examiner intelligence with evidence intake, framework mapping rationale, finding register export, and local review history.</p>
        </div>
        <div className="heroCard">
          <span>Sentinel v1.0</span>
          <strong>Consulting-Ready Assurance Console</strong>
          <p>Upload JSON, CSV, or text evidence packages and convert them into examiner-ready review input.</p>
        </div>
      </section>

      <section className="caseLibrary">
        <div>
          <h2>Evidence Intake</h2>
          <p>Upload JSON, CSV, or text evidence. Sentinel converts it into a structured review package.</p>
        </div>
        <div className="uploadBox">
          <input type="file" accept=".json,.csv,.txt,.md" onChange={handleFileUpload} />
          <span>Supported: JSON packages, CSV rows, TXT/MD evidence notes</span>
        </div>
      </section>

      <section className="caseLibrary">
        <div>
          <h2>Sample Case Library</h2>
          <p>Load realistic regulated-industry evidence packages and run examiner review.</p>
        </div>
        <div className="caseGrid">
          {Object.keys(cases).map((name) => (
            <button key={name} className={selectedCase === name ? "caseCard active" : "caseCard"} onClick={() => loadCase(name)}>
              <strong>{name}</strong>
              <span>
                {name === "IT Metrics Examiner" && "Denominator, evidence lineage, and reporting validation."}
                {name === "Vendor & Privacy Examiner" && "SOC 2 reliance, CUEC, NPI/PII, data-flow, and retention challenge."}
                {name === "SDLC & AI Governance Examiner" && "Release governance, AI approval, security gates, and production-readiness challenge."}
                {name === "IAM Evidence Examiner" && "Access governance, authentication, MFA, exception, and review evidence challenge."}
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Evidence Input</h2>
          <p className="muted">Paste, load, or upload evidence package JSON. Sentinel will challenge evidence quality, metric logic, and governance defensibility.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button className="primaryBtn" onClick={analyze}>Run Examiner Review</button>
          {error && <div className="error">{error}</div>}

          {history.length > 0 && (
            <div className="historyBox">
              <div className="historyHead">
                <h3>Local Review History</h3>
                <button onClick={clearHistory}>Clear</button>
              </div>
              {history.map((h, idx) => (
                <div key={idx} className="historyRow">
                  <strong>{h.evidence_type}</strong>
                  <span>{h.rating} Ã‚Â· {h.score}/100 Ã‚Â· {h.findings} findings</span>
                  <em>{new Date(h.timestamp).toLocaleString()}</em>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="panel">
          <h2>Examiner Output</h2>
          <p className="muted">Executive-ready findings, evidence gaps, challenge questions, remediation guidance, and framework mapping rationale.</p>

          {!result && <div className="empty">Run the examiner review to generate assurance score, severity distribution, framework coverage, and exportable report.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Assurance Score</span><strong>{result.assurance_score}/100</strong></div>
                <div className="scoreBox"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                <div className="scoreBox"><span>Findings</span><strong>{result.total_findings}</strong></div>
              </div>

              <div className="actions">
                <button onClick={downloadJson}>Download JSON</button>
                <button onClick={downloadFindingRegisterCsv}>Finding Register</button>
                <button onClick={downloadHtmlReport}>HTML Report</button>
                <button onClick={copySummary}>Copy Summary</button>
                <button onClick={() => window.print()}>Print</button>
              </div>

              <div className="summary">{result.executive_summary}</div>

              <div className="miniGrid">
                <div>
                  <h3>Severity Distribution</h3>
                  {Object.entries(result.severity_distribution || {}).map(([k, v]: any) => (
                    <div key={k} className="miniRow"><span>{k}</span><strong>{v}</strong></div>
                  ))}
                </div>
                <div>
                  <h3>Top Risk Domains</h3>
                  {(result.top_risk_domains || []).map((x: any) => (
                    <div key={x.domain} className="miniRow"><span>{x.domain}</span><strong>{x.count}</strong></div>
                  ))}
                </div>
              </div>

              <div className="nextSteps">
                <h3>Framework Coverage</h3>
                {(result.framework_coverage || []).map((x: any) => (
                  <div key={x.framework} className="miniRow"><span>{x.framework}</span><strong>{x.count}</strong></div>
                ))}
              </div>

              <div className="nextSteps">
                <h3>Recommended Next Steps</h3>
                <ol>{(result.recommended_next_steps || []).map((step: string) => <li key={step}>{step}</li>)}</ol>
              </div>

              <div className="findings">
                {result.findings.map((finding: any, index: number) => (
                  <div key={index} className="finding">
                    <div className="findingTop">
                      <h3>{finding.title}</h3>
                      <span className={"badge " + finding.severity.toLowerCase()}>{finding.severity}</span>
                    </div>
                    <p><b>Risk domain:</b> {finding.risk_domain}</p>
                    <p><b>Affected item:</b> {finding.affected_item}</p>
                    <p><b>Issue:</b> {finding.issue}</p>
                    <p><b>Evidence gap:</b> {finding.evidence_gap}</p>
                    <p><b>Examiner question:</b> {finding.examiner_question}</p>
                    <p><b>Remediation:</b> {finding.remediation}</p>

                    <div className="mappingBox">
                      <h4>Framework Mapping Rationale</h4>
                      {(finding.framework_mappings || []).map((m: any) => (
                        <div key={m.framework} className="mappingRow">
                          <strong>{m.framework}</strong>
                          <span>{m.mapping_type}</span>
                          <p>{m.rationale}</p>
                          <em>Expected evidence: {m.evidence_expected}</em>
                        </div>
                      ))}
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
