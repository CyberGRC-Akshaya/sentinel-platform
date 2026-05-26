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
  }
};

type RegisterRow = {
  finding_id: string;
  severity: string;
  risk_domain: string;
  affected_item: string;
  issue: string;
  remediation: string;
  evidence_needed: string;
  preferred_artifacts: string;
  owner: string;
  target_date: string;
  status: string;
  management_response: string;
  closure_evidence: string;
  validation_notes: string;
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
  const [registerRows, setRegisterRows] = useState<RegisterRow[]>([]);
  const [reviews, setReviews] = useState<any[]>([]);
  const [currentReviewId, setCurrentReviewId] = useState("");
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("Workbench");
  const [saveMessage, setSaveMessage] = useState("");

  useEffect(() => {
    loadVault();
  }, []);

  async function loadVault() {
    try {
      const response = await fetch(`${API_BASE}/api/reviews`);
      if (response.ok) {
        const data = await response.json();
        setReviews(data);
      }
    } catch {
      setReviews([]);
    }
  }

  function loadCase(name: string) {
    setSelectedCase(name);
    setInput(JSON.stringify(cases[name], null, 2));
    setResult(null);
    setRegisterRows([]);
    setCurrentReviewId("");
    setActiveTab("Workbench");
    setError("");
    setSaveMessage("");
  }

  function smartSplitCsv(line: string) {
    const result: string[] = [];
    let current = "";
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"') inQuotes = !inQuotes;
      else if (char === "," && !inQuotes) {
        result.push(current.trim().replace(/^"|"$/g, ""));
        current = "";
      } else current += char;
    }
    result.push(current.trim().replace(/^"|"$/g, ""));
    return result;
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
      setRegisterRows([]);
      setCurrentReviewId("");
      setActiveTab("Workbench");
    } catch (err: any) {
      setError("Could not parse uploaded file: " + err.message);
    }
  }

  async function analyzeAndSave() {
    setError("");
    setResult(null);
    setRegisterRows([]);
    setSaveMessage("");
    try {
      const payload = JSON.parse(input);
      const response = await fetch(`${API_BASE}/api/reviews/analyze-save`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error("Backend returned error: " + response.status);
      const data = await response.json();
      setResult(data);
      setCurrentReviewId(data.review_id || "");
      setRegisterRows(data.remediation_register || []);
      setActiveTab("Command Center");
      setSaveMessage("Review saved to vault.");
      await loadVault();
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    }
  }

  async function loadSavedReview(reviewId: string) {
    setError("");
    try {
      const response = await fetch(`${API_BASE}/api/reviews/${reviewId}`);
      if (!response.ok) throw new Error("Review not found.");
      const data = await response.json();
      setResult(data);
      setCurrentReviewId(reviewId);
      setRegisterRows(data.remediation_register || []);
      setActiveTab("Command Center");
      setSaveMessage("Saved review loaded from vault.");
    } catch (err: any) {
      setError(err.message || "Could not load review.");
    }
  }

  async function deleteSavedReview(reviewId: string) {
    try {
      await fetch(`${API_BASE}/api/reviews/${reviewId}`, { method: "DELETE" });
      if (currentReviewId === reviewId) {
        setCurrentReviewId("");
        setResult(null);
        setRegisterRows([]);
      }
      await loadVault();
    } catch {
      setError("Could not delete review.");
    }
  }

  async function saveRegister() {
    if (!currentReviewId) {
      setSaveMessage("Run a saved review first.");
      return;
    }

    const response = await fetch(`${API_BASE}/api/reviews/${currentReviewId}/register`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ rows: registerRows })
    });

    if (response.ok) {
      setSaveMessage("Register saved to review vault.");
      await loadVault();
    } else {
      setSaveMessage("Register save failed.");
    }
  }

  function updateRegisterRow(index: number, field: keyof RegisterRow, value: string) {
    const next = [...registerRows];
    next[index] = { ...next[index], [field]: value };
    setRegisterRows(next);
  }

  function csvEscape(value: any) {
    const text = String(value ?? "");
    return `"${text.replace(/"/g, '""')}"`;
  }

  function downloadCsv(fileName: string, headers: string[], rows: any[][]) {
    const csv = [headers, ...rows].map((row) => row.map(csvEscape).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadWorkspaceJson() {
    if (!result) return;
    const payload = { ...result, remediation_register: registerRows };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v3-review-vault-workspace.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadRegisterCsv() {
    const headers = [
      "Finding_ID","Severity","Risk_Domain","Affected_Item","Issue","Remediation","Evidence_Needed",
      "Preferred_Artifacts","Owner","Target_Date","Status","Management_Response","Closure_Evidence","Validation_Notes"
    ];

    const rows = registerRows.map((row) => [
      row.finding_id,row.severity,row.risk_domain,row.affected_item,row.issue,row.remediation,row.evidence_needed,
      row.preferred_artifacts,row.owner,row.target_date,row.status,row.management_response,row.closure_evidence,row.validation_notes
    ]);

    downloadCsv("sentinel-v3-remediation-register.csv", headers, rows);
  }

  function downloadIntakeCsv() {
    if (!result) return;
    const headers = ["Item","Domain","Artifact_Type","Metadata_Score","Missing_Metadata","Intake_Score","Intake_Rating","Missing_Elements"];
    const rows = result.item_scorecards.map((item: any) => [
      item.item_title,
      item.domain,
      item.artifact_profile?.artifact_type || "",
      item.artifact_profile?.metadata_completeness_score || "",
      (item.artifact_profile?.missing_metadata || []).join("; "),
      item.intake_gap_analysis?.intake_coverage_score || "",
      item.intake_gap_analysis?.intake_rating || "",
      (item.intake_gap_analysis?.missing_elements || []).join("; ")
    ]);
    downloadCsv("sentinel-v3-intake-diagnostics.csv", headers, rows);
  }

  async function downloadHtmlReport() {
    if (!result) return;
    try {
      let response;
      if (currentReviewId) {
        response = await fetch(`${API_BASE}/api/reviews/${currentReviewId}/report-html`);
      } else {
        const payload = JSON.parse(input);
        response = await fetch(`${API_BASE}/api/report-html`, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload)
        });
      }
      const reportHtml = await response.text();
      const blob = new Blob([reportHtml], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "sentinel-v3-evidence-defensibility-report.html";
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

  function registerStats() {
    const open = registerRows.filter((r) => r.status === "Open").length;
    const inProgress = registerRows.filter((r) => r.status === "In Progress").length;
    const pending = registerRows.filter((r) => r.status === "Pending Evidence").length;
    const riskAccepted = registerRows.filter((r) => r.status === "Risk Accepted").length;
    const closed = registerRows.filter((r) => r.status === "Closed").length;
    return { open, inProgress, pending, riskAccepted, closed };
  }

  const stats = registerStats();

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Eye On Bits Pvt Ltd · Sentinel v3.0</p>
          <h1>Evidence Defensibility Workbench</h1>
          <p className="subtitle">
            Professional assurance workbench with persistent review vault, intake diagnostics, defensibility scoring,
            remediation register, and saved report workspace.
          </p>
        </div>
        <div className="heroCard">
          <span>Major Upgrade</span>
          <strong>Persistent Review Vault + Saved Remediation Register.</strong>
          <p>Run reviews, save them locally, reopen them after restart, update management responses, and export client-ready registers.</p>
        </div>
      </section>

      <section className="caseLibrary">
        <div>
          <h2>Evidence Intake</h2>
          <p>Upload JSON, CSV, TXT, or MD evidence. Sentinel converts it into a structured review package.</p>
        </div>
        <div className="uploadBox">
          <input type="file" accept=".json,.csv,.txt,.md" onChange={handleFileUpload} />
          <span>v3.0 stores saved reviews in a local SQLite vault under backend/data.</span>
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
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Review Input</h2>
          <p className="muted">Paste, load, or upload evidence package JSON. Sentinel will save the review into the local vault.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button className="primaryBtn" onClick={analyzeAndSave}>Run + Save Review to Vault</button>
          {error && <div className="error">{error}</div>}
          {saveMessage && <div className="summary">{saveMessage}</div>}

          <div className="historyBox">
            <div className="historyHead">
              <h3>Review Vault</h3>
              <button onClick={loadVault}>Refresh</button>
            </div>
            {reviews.length === 0 && <p className="muted">No saved reviews yet.</p>}
            {reviews.map((review) => (
              <div key={review.id} className="vaultRow">
                <strong>{review.evidence_type}</strong>
                <span>{review.organization} · {review.overall_rating} · {review.evidence_defensibility_score}/100 · {review.total_findings} findings</span>
                <em>{new Date(review.created_at).toLocaleString()}</em>
                <div className="vaultActions">
                  <button onClick={() => loadSavedReview(review.id)}>Load</button>
                  <button onClick={() => deleteSavedReview(review.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h2>Saved Review Workspace</h2>
          <p className="muted">Scorecards, intake diagnostics, evidence requests, and persistent remediation register.</p>

          {!result && <div className="empty">Run a review or load one from the Review Vault.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Defensibility</span><strong>{result.evidence_defensibility_score}/100</strong></div>
                <div className="scoreBox"><span>Intake Coverage</span><strong>{result.intake_coverage_score}/100</strong></div>
                <div className="scoreBox"><span>Metadata</span><strong>{result.metadata_completeness_score}/100</strong></div>
              </div>

              <div className="tabBar">
                {["Command Center", "Output", "Scorecards", "Findings"].map((tab) => (
                  <button key={tab} className={activeTab === tab ? "tab activeTab" : "tab"} onClick={() => setActiveTab(tab)}>{tab}</button>
                ))}
              </div>

              <div className="actions">
                <button onClick={saveRegister}>Save Register</button>
                <button onClick={downloadWorkspaceJson}>Workspace JSON</button>
                <button onClick={downloadRegisterCsv}>Register CSV</button>
                <button onClick={downloadIntakeCsv}>Intake CSV</button>
                <button onClick={downloadHtmlReport}>HTML Report</button>
              </div>

              <div className="actions secondaryActions">
                <button onClick={copySummary}>Copy Executive Summary</button>
              </div>

              {activeTab === "Command Center" && (
                <div>
                  <div className="summary">{result.executive_summary}</div>
                  <div className="miniGrid">
                    <div>
                      <h3>Remediation Status</h3>
                      <div className="miniRow"><span>Open</span><strong>{stats.open}</strong></div>
                      <div className="miniRow"><span>In Progress</span><strong>{stats.inProgress}</strong></div>
                      <div className="miniRow"><span>Pending Evidence</span><strong>{stats.pending}</strong></div>
                      <div className="miniRow"><span>Risk Accepted</span><strong>{stats.riskAccepted}</strong></div>
                      <div className="miniRow"><span>Closed</span><strong>{stats.closed}</strong></div>
                    </div>
                    <div>
                      <h3>Vault Metadata</h3>
                      <div className="miniRow"><span>Review ID</span><strong>{currentReviewId ? currentReviewId.slice(0, 8) : "Unsaved"}</strong></div>
                      <div className="miniRow"><span>Total Findings</span><strong>{result.total_findings}</strong></div>
                      <div className="miniRow"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                    </div>
                  </div>

                  <div className="registerPanel">
                    <h3>Persistent Remediation Register</h3>
                    <p className="muted">Update fields, click Save Register, then reload from vault to confirm persistence.</p>
                    {registerRows.map((row, index) => (
                      <div key={row.finding_id} className="registerCard">
                        <div className="registerHeader">
                          <strong>{row.finding_id} · {row.severity} · {row.risk_domain}</strong>
                          <span>{row.affected_item}</span>
                        </div>
                        <p><b>Issue:</b> {row.issue}</p>
                        <p><b>Evidence needed:</b> {row.evidence_needed}</p>
                        <div className="registerGrid">
                          <label>Owner<input value={row.owner} onChange={(e) => updateRegisterRow(index, "owner", e.target.value)} /></label>
                          <label>Target Date<input type="date" value={row.target_date} onChange={(e) => updateRegisterRow(index, "target_date", e.target.value)} /></label>
                          <label>Status
                            <select value={row.status} onChange={(e) => updateRegisterRow(index, "status", e.target.value)}>
                              <option>Open</option>
                              <option>In Progress</option>
                              <option>Pending Evidence</option>
                              <option>Risk Accepted</option>
                              <option>Closed</option>
                            </select>
                          </label>
                        </div>
                        <label>Management Response
                          <textarea className="smallText" value={row.management_response} onChange={(e) => updateRegisterRow(index, "management_response", e.target.value)} />
                        </label>
                        <label>Closure Evidence
                          <textarea className="smallText" value={row.closure_evidence} onChange={(e) => updateRegisterRow(index, "closure_evidence", e.target.value)} />
                        </label>
                        <label>Validation Notes
                          <textarea className="smallText" value={row.validation_notes} onChange={(e) => updateRegisterRow(index, "validation_notes", e.target.value)} />
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === "Output" && (
                <div>
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
                </div>
              )}

              {activeTab === "Scorecards" && (
                <div className="nextSteps">
                  <h3>Item Scorecards + Intake Diagnostics</h3>
                  {(result.item_scorecards || []).map((item: any) => (
                    <div key={item.item_title} className="scorecardItem">
                      <div className="scorecardTop">
                        <strong>{item.item_title}</strong>
                        <span>{item.score}/100 · {item.rating}</span>
                      </div>
                      <p>{item.domain} · {item.artifact_profile?.artifact_type}</p>
                      <div className="miniRow"><span>Metadata completeness</span><strong>{item.artifact_profile?.metadata_completeness_score}/100</strong></div>
                      <div className="miniRow"><span>Intake coverage</span><strong>{item.intake_gap_analysis?.intake_coverage_score}/100</strong></div>
                      {(item.artifact_profile?.missing_metadata || []).length > 0 && <p><b>Missing metadata:</b> {(item.artifact_profile?.missing_metadata || []).join(", ")}</p>}
                      {(item.intake_gap_analysis?.missing_elements || []).length > 0 && <p><b>Missing intake elements:</b> {(item.intake_gap_analysis?.missing_elements || []).join(", ")}</p>}
                      {(item.dimensions || []).map((d: any) => (
                        <div key={d.key} className="dimensionRow"><span>{d.label}</span><strong>{d.score}/100</strong><em>{d.rating}</em></div>
                      ))}
                    </div>
                  ))}
                </div>
              )}

              {activeTab === "Findings" && (
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
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
