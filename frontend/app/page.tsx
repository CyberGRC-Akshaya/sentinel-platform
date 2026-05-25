"use client";

import { useState } from "react";

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
  }
};

export default function Home() {
  const [selectedCase, setSelectedCase] = useState("IT Metrics Examiner");
  const [input, setInput] = useState(JSON.stringify(cases["IT Metrics Examiner"], null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  function loadCase(name: string) {
    setSelectedCase(name);
    setInput(JSON.stringify(cases[name], null, 2));
    setResult(null);
    setError("");
  }

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
      setResult(await response.json());
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    }
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

  function csvEscape(value: any) {
    const text = String(value ?? "");
    return `"${text.replace(/"/g, '""')}"`;
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
      "",
      "",
      "Open",
      ""
    ]);

    const csv = [headers, ...rows]
      .map((row) => row.map(csvEscape).join(","))
      .join("\n");

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
      const response = await fetch("http://localhost:8000/api/report-html", {
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

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Eye On Bits Pvt Ltd</p>
          <h1>Sentinel Assurance Platform</h1>
          <p className="subtitle">AI-native examiner intelligence for metrics validation, evidence challenge, control assurance, vendor risk, privacy, SDLC, and AI governance review.</p>
        </div>
        <div className="heroCard">
          <span>Sentinel v0.7</span>
          <strong>Finding Register Console</strong>
          <p>Built for BFSI, audit, GRC, privacy, TPRM, AI governance, and SDLC assurance workflows.</p>
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
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Evidence Input</h2>
          <p className="muted">Paste or load evidence package JSON. Sentinel will challenge evidence quality, metric logic, and governance defensibility.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button className="primaryBtn" onClick={analyze}>Run Examiner Review</button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="panel">
          <h2>Examiner Output</h2>
          <p className="muted">Executive-ready findings, evidence gaps, challenge questions, and remediation guidance.</p>

          {!result && <div className="empty">Run the examiner review to generate assurance score, severity distribution, top risk domains, and exportable report.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Assurance Score</span><strong>{result.assurance_score}/100</strong></div>
                <div className="scoreBox"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                <div className="scoreBox"><span>Findings</span><strong>{result.total_findings}</strong></div>
              </div>

              <div className="actions">
                <button onClick={downloadJson}>Download JSON</button>
                <button onClick={downloadFindingRegisterCsv}>Download Finding Register</button>
                <button onClick={downloadHtmlReport}>Download HTML Report</button>
                <button onClick={copySummary}>Copy Summary</button>
                <button onClick={() => window.print()}>Print Screen</button>
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
