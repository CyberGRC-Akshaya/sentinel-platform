"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const cases: Record<string, any> = {
  "IT Metrics Evidence Package": {
    organization: "Sample Tier-1 Bank",
    industry: "BFSI / Regulated Banking",
    evidence_type: "IT Metrics Defensibility Review",
    review_objective: "Assess whether IT metrics evidence supports denominator consistency, source lineage, calculation integrity, reporting-period alignment, and management review.",
    items: [
      {
        title: "Q4 Phishing Metric Evidence",
        content: "The ITSC deck reported 150 delivered emails. KnowBe4 source export shows denominator changed to 152. Screenshot-only evidence was retained. Metric owner stated the number was corrected later. No reviewer approval or reconciliation is attached.",
        source_system: "KnowBe4 / ITSC Deck",
        owner: "IT GRC",
        reporting_period: "Q4",
        evidence_date: "",
        control_reference: ""
      },
      {
        title: "RCSA Control Effectiveness Metric",
        content: "The reported value was presented as quarterly, but calculation logic appears cumulative year-to-date. The metric narrative says effective and green but does not show test procedure, sample basis, or reviewer approval.",
        source_system: "RCSA Tracker",
        owner: "Risk Management",
        reporting_period: "Q3",
        evidence_date: "",
        control_reference: ""
      }
    ]
  },
  "Vendor Privacy Evidence Package": {
    organization: "Sample Financial Institution",
    industry: "BFSI / Vendor Risk",
    evidence_type: "Vendor and Privacy Evidence Defensibility Review",
    review_objective: "Assess SOC 2 reliance, CUEC analysis, data-flow evidence, retention, customer information handling, and residual risk support.",
    items: [
      {
        title: "Vendor SOC 2 and Data Handling Evidence",
        content: "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, bridge letter, subservice organization review, DPA, or CUEC analysis.",
        source_system: "Vendor Portal",
        owner: "TPRM",
        reporting_period: "Annual Review",
        evidence_date: "",
        control_reference: ""
      }
    ]
  },
  "SDLC AI Release Package": {
    organization: "Sample Enterprise Technology Group",
    industry: "Technology / AI Governance",
    evidence_type: "SDLC and AI Governance Defensibility Review",
    review_objective: "Assess release governance, AI approval, security gates, production readiness, monitoring, and incident escalation evidence.",
    items: [
      {
        title: "AI-Enabled Release Evidence",
        content: "Release notes mention AI assistant functionality and production rollout. Evidence includes release summary but no AI inventory entry, risk tier, approval record, security gate, change record, risk acceptance, monitoring plan, or incident escalation logic.",
        source_system: "DevOps Release Tracker",
        owner: "Application Owner",
        reporting_period: "Release 2026.05",
        evidence_date: "",
        control_reference: ""
      }
    ]
  },
  "IAM Authentication Evidence Package": {
    organization: "Sample Bank IAM Program",
    industry: "BFSI / Identity and Access",
    evidence_type: "IAM and Authentication Evidence Defensibility Review",
    review_objective: "Assess access governance, authentication coverage, MFA evidence, approval, periodic review, exception handling, and remediation tracking.",
    items: [
      {
        title: "Customer Access and MFA Evidence",
        content: "IAM evidence references customer access, authentication, MFA, and access review activity. Evidence does not show full approval trail, risk-based exception handling, periodic review results, issue remediation, or closure evidence.",
        source_system: "IAM Review Tracker",
        owner: "IAM Governance",
        reporting_period: "Quarterly Review",
        evidence_date: "",
        control_reference: ""
      }
    ]
  }
};

function defaultIntakePayload() {
  return {
    organization: "Imported Evidence Package",
    industry: "Regulated Enterprise",
    evidence_type: "Uploaded Evidence Defensibility Review",
    review_objective: "Challenge uploaded evidence for assurance readiness, evidence lineage, governance defensibility, and examiner-style gaps.",
    items: []
  };
}

export default function Home() {
  const [selectedCase, setSelectedCase] = useState("IT Metrics Evidence Package");
  const [input, setInput] = useState(JSON.stringify(cases["IT Metrics Evidence Package"], null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem("sentinel-v21-review-history");
    if (saved) {
      try { setHistory(JSON.parse(saved)); } catch { setHistory([]); }
    }
  }, []);

  function saveHistory(entry: any) {
    const next = [entry, ...history].slice(0, 10);
    setHistory(next);
    localStorage.setItem("sentinel-v21-review-history", JSON.stringify(next));
  }

  function loadCase(name: string) {
    setSelectedCase(name);
    setInput(JSON.stringify(cases[name], null, 2));
    setResult(null);
    setError("");
  }

  function buildTextPayload(fileName: string, text: string) {
    const payload = defaultIntakePayload();
    payload.items = [{
      title: fileName,
      content: text.slice(0, 25000),
      source_system: "Uploaded File",
      owner: "Evidence Submitter",
      reporting_period: "Uploaded Review",
      artifact_type: fileName.toLowerCase().endsWith(".md") ? "Markdown Evidence Note" : "Text Evidence Note",
      evidence_date: "",
      control_reference: ""
    }];
    return payload;
  }

  function smartSplitCsv(line: string) {
    const result: string[] = [];
    let current = "";
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === "," && !inQuotes) {
        result.push(current.trim().replace(/^"|"$/g, ""));
        current = "";
      } else {
        current += char;
      }
    }
    result.push(current.trim().replace(/^"|"$/g, ""));
    return result;
  }

  function parseCsvToPayload(fileName: string, text: string) {
    const lines = text.split(/\r?\n/).filter(Boolean);
    const payload = defaultIntakePayload();
    payload.evidence_type = "Uploaded CSV Evidence Defensibility Review";

    if (lines.length === 0) return payload;

    const headers = smartSplitCsv(lines[0]).map((h) => h.trim());
    const rows = lines.slice(1).slice(0, 50);

    payload.items = rows.map((line, index) => {
      const cols = smartSplitCsv(line);
      const obj: Record<string, string> = {};
      headers.forEach((h, i) => { obj[h || `Column_${i + 1}`] = cols[i] || ""; });

      return {
        title: obj.title || obj.Title || obj.name || obj.Name || `CSV Evidence Row ${index + 1}`,
        content: obj.content || obj.Content || obj.description || obj.Description || JSON.stringify(obj),
        source_system: obj.source_system || obj.Source_System || obj.Source || obj.source || "Uploaded CSV",
        owner: obj.owner || obj.Owner || "Evidence Submitter",
        reporting_period: obj.reporting_period || obj.Reporting_Period || obj.period || "Uploaded Review",
        artifact_type: obj.artifact_type || obj.Artifact_Type || "CSV Evidence Row",
        evidence_date: obj.evidence_date || obj.Evidence_Date || obj.date || "",
        control_reference: obj.control_reference || obj.Control_Reference || obj.control || ""
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
            reporting_period: item.reporting_period || "Uploaded Review",
            artifact_type: item.artifact_type || "JSON Evidence Item",
            evidence_date: item.evidence_date || "",
            control_reference: item.control_reference || ""
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
        score: data.evidence_defensibility_score,
        intake: data.intake_coverage_score,
        metadata: data.metadata_completeness_score,
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
    a.download = "sentinel-v2.1-evidence-report.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadFindingRegisterCsv() {
    if (!result) return;
    const headers = [
      "Finding_ID","Severity","Severity_Rationale","Risk_Domain","Dimension","Affected_Item","Issue","Evidence_Gap",
      "Examiner_Question","Remediation","Framework_Relevance","Framework_Rationale","Expected_Evidence",
      "Evidence_Request_ID","Evidence_Needed","Preferred_Artifacts","Owner","Target_Date","Status","Management_Response"
    ];

    const rows = result.findings.map((finding: any) => [
      finding.finding_id,
      finding.severity,
      finding.severity_rationale,
      finding.risk_domain,
      finding.dimension,
      finding.affected_item,
      finding.issue,
      finding.evidence_gap,
      finding.examiner_question,
      finding.remediation,
      (finding.framework_relevance || []).join("; "),
      (finding.framework_mappings || []).map((m: any) => `${m.framework}: ${m.rationale}`).join(" | "),
      (finding.framework_mappings || []).map((m: any) => `${m.framework}: ${m.evidence_expected}`).join(" | "),
      finding.evidence_request?.request_id || "",
      finding.evidence_request?.evidence_needed || "",
      (finding.evidence_request?.preferred_artifacts || []).join("; "),
      finding.evidence_request?.owner || "",
      "",
      "Open",
      ""
    ]);

    const csv = [headers, ...rows].map((row) => row.map(csvEscape).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v2.1-finding-register.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadEvidenceRequestCsv() {
    if (!result) return;
    const headers = ["Request_ID","Priority","Owner","Evidence_Needed","Preferred_Artifacts","Status"];
    const rows = result.evidence_requests.map((req: any) => [
      req.request_id,
      req.priority,
      req.owner,
      req.evidence_needed,
      (req.preferred_artifacts || []).join("; "),
      req.status
    ]);

    const csv = [headers, ...rows].map((row) => row.map(csvEscape).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v2.1-evidence-request-list.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadIntakeDiagnosticsCsv() {
    if (!result) return;
    const headers = [
      "Item",
      "Domain",
      "Artifact_Type",
      "Metadata_Completeness_Score",
      "Missing_Metadata",
      "Intake_Coverage_Score",
      "Intake_Rating",
      "Present_Elements",
      "Missing_Elements"
    ];

    const rows = result.item_scorecards.map((item: any) => [
      item.item_title,
      item.domain,
      item.artifact_profile?.artifact_type || "",
      item.artifact_profile?.metadata_completeness_score || "",
      (item.artifact_profile?.missing_metadata || []).join("; "),
      item.intake_gap_analysis?.intake_coverage_score || "",
      item.intake_gap_analysis?.intake_rating || "",
      (item.intake_gap_analysis?.present_elements || []).join("; "),
      (item.intake_gap_analysis?.missing_elements || []).join("; ")
    ]);

    const csv = [headers, ...rows].map((row) => row.map(csvEscape).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v2.1-intake-diagnostics.csv";
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
      a.download = "sentinel-v2.1-evidence-defensibility-report.html";
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
    localStorage.removeItem("sentinel-v21-review-history");
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Eye On Bits Pvt Ltd · Sentinel v2.1</p>
          <h1>Evidence Defensibility Workbench</h1>
          <p className="subtitle">
            Professional assurance workbench for evidence quality, intake coverage, metadata completeness,
            source lineage, calculation integrity, governance traceability, and framework relevance.
          </p>
        </div>
        <div className="heroCard">
          <span>Positioning</span>
          <strong>Evidence intake intelligence + defensibility challenge layer.</strong>
          <p>Built for IT GRC, audit readiness, TPRM, privacy, SDLC, IAM, and AI governance evidence reviews.</p>
        </div>
      </section>

      <section className="caseLibrary">
        <div>
          <h2>Evidence Intake</h2>
          <p>Upload JSON, CSV, TXT, or MD evidence. Sentinel converts it into a structured review package and evaluates metadata quality.</p>
        </div>
        <div className="uploadBox">
          <input type="file" accept=".json,.csv,.txt,.md" onChange={handleFileUpload} />
          <span>v2.1 supports smarter CSV parsing, artifact typing, intake diagnostics, and metadata completeness scoring.</span>
        </div>
      </section>

      <section className="caseLibrary">
        <div>
          <h2>Professional Sample Packages</h2>
          <p>Each package demonstrates a real assurance review pattern.</p>
        </div>
        <div className="caseGrid">
          {Object.keys(cases).map((name) => (
            <button key={name} className={selectedCase === name ? "caseCard active" : "caseCard"} onClick={() => loadCase(name)}>
              <strong>{name}</strong>
              <span>
                {name === "IT Metrics Evidence Package" && "Metric denominator, lineage, review, and reporting-period challenge."}
                {name === "Vendor Privacy Evidence Package" && "SOC 2 reliance, CUEC, customer data, retention, and data-flow challenge."}
                {name === "SDLC AI Release Package" && "Release governance, AI approval, security gate, monitoring, and change evidence challenge."}
                {name === "IAM Authentication Evidence Package" && "Access governance, MFA, exception, review, and remediation evidence challenge."}
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Review Input</h2>
          <p className="muted">Paste, load, or upload evidence package JSON. Sentinel will produce scorecards, intake diagnostics, findings, and evidence requests.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button className="primaryBtn" onClick={analyze}>Run Evidence Defensibility Review</button>
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
                  <span>{h.rating} · Defensibility {h.score}/100 · Intake {h.intake}/100 · Metadata {h.metadata}/100</span>
                  <em>{new Date(h.timestamp).toLocaleString()}</em>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="panel">
          <h2>Defensibility Output</h2>
          <p className="muted">Scorecards, intake diagnostics, evidence requests, severity rationale, and framework mapping rationale.</p>

          {!result && <div className="empty">Run a review to generate professional evidence defensibility output.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Defensibility</span><strong>{result.evidence_defensibility_score}/100</strong></div>
                <div className="scoreBox"><span>Intake Coverage</span><strong>{result.intake_coverage_score}/100</strong></div>
                <div className="scoreBox"><span>Metadata</span><strong>{result.metadata_completeness_score}/100</strong></div>
              </div>

              <div className="actions">
                <button onClick={downloadJson}>JSON</button>
                <button onClick={downloadFindingRegisterCsv}>Findings</button>
                <button onClick={downloadEvidenceRequestCsv}>Requests</button>
                <button onClick={downloadIntakeDiagnosticsCsv}>Intake CSV</button>
                <button onClick={downloadHtmlReport}>HTML</button>
              </div>

              <div className="actions secondaryActions">
                <button onClick={copySummary}>Copy Summary</button>
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
                <h3>Item Scorecards + Intake Diagnostics</h3>
                {(result.item_scorecards || []).map((item: any) => (
                  <div key={item.item_title} className="scorecardItem">
                    <div className="scorecardTop">
                      <strong>{item.item_title}</strong>
                      <span>{item.score}/100 · {item.rating}</span>
                    </div>
                    <p>{item.domain} · {item.artifact_profile?.artifact_type}</p>
                    <div className="miniRow">
                      <span>Metadata completeness</span>
                      <strong>{item.artifact_profile?.metadata_completeness_score}/100</strong>
                    </div>
                    <div className="miniRow">
                      <span>Intake coverage</span>
                      <strong>{item.intake_gap_analysis?.intake_coverage_score}/100</strong>
                    </div>
                    {(item.artifact_profile?.missing_metadata || []).length > 0 && (
                      <p><b>Missing metadata:</b> {(item.artifact_profile?.missing_metadata || []).join(", ")}</p>
                    )}
                    {(item.intake_gap_analysis?.missing_elements || []).length > 0 && (
                      <p><b>Missing intake elements:</b> {(item.intake_gap_analysis?.missing_elements || []).join(", ")}</p>
                    )}
                    {(item.dimensions || []).map((d: any) => (
                      <div key={d.key} className="dimensionRow">
                        <span>{d.label}</span>
                        <strong>{d.score}/100</strong>
                        <em>{d.rating}</em>
                      </div>
                    ))}
                  </div>
                ))}
              </div>

              <div className="nextSteps">
                <h3>Evidence Request List</h3>
                {(result.evidence_requests || []).map((req: any) => (
                  <div key={req.request_id} className="requestRow">
                    <strong>{req.request_id} · {req.priority}</strong>
                    <span>{req.evidence_needed}</span>
                    <em>Preferred: {(req.preferred_artifacts || []).join(", ")}</em>
                  </div>
                ))}
              </div>

              <div className="findings">
                {result.findings.map((finding: any) => (
                  <div key={finding.finding_id} className="finding">
                    <div className="findingTop">
                      <h3>{finding.finding_id} — {finding.title}</h3>
                      <span className={"badge " + finding.severity.toLowerCase()}>{finding.severity}</span>
                    </div>
                    <p><b>Risk domain:</b> {finding.risk_domain}</p>
                    <p><b>Dimension:</b> {finding.dimension}</p>
                    <p><b>Affected item:</b> {finding.affected_item}</p>
                    <p><b>Issue:</b> {finding.issue}</p>
                    <p><b>Severity rationale:</b> {finding.severity_rationale}</p>
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

              <div className="nextSteps">
                <h3>Recommended Next Steps</h3>
                <ol>{(result.recommended_next_steps || []).map((step: string) => <li key={step}>{step}</li>)}</ol>
              </div>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
