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
        artifact_type: "Metric Evidence"
      },
      {
        title: "RCSA Control Effectiveness Metric",
        content: "The reported value was presented as quarterly, but calculation logic appears cumulative year-to-date. The metric narrative says effective and green but does not show test procedure, sample basis, or reviewer approval.",
        source_system: "RCSA Tracker",
        owner: "Risk Management",
        reporting_period: "Q3",
        artifact_type: "Metric Evidence"
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
        artifact_type: "SOC 2 / Vendor Evidence"
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
        artifact_type: "AI Release Evidence"
      }
    ]
  }
};

type RegisterRow = {
  finding_id: string;
  severity: string;
  risk_domain: string;
  control_atlas_ids?: string;
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
  const [portfolio, setPortfolio] = useState<any>(null);
  const [currentReviewId, setCurrentReviewId] = useState("");
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("Workbench");
  const [saveMessage, setSaveMessage] = useState("");

  useEffect(() => {
    loadVault();
    loadPortfolio();
  }, []);

  async function loadVault() {
    try {
      const response = await fetch(`${API_BASE}/api/reviews`);
      if (response.ok) setReviews(await response.json());
    } catch {
      setReviews([]);
    }
  }

  async function loadPortfolio() {
    try {
      const response = await fetch(`${API_BASE}/api/portfolio`);
      if (response.ok) setPortfolio(await response.json());
    } catch {
      setPortfolio(null);
    }
  }

  async function seedDemoReviews() {
    setSaveMessage("");
    try {
      const response = await fetch(`${API_BASE}/api/demo/seed`, { method: "POST" });
      if (!response.ok) throw new Error("Could not seed demo reviews.");
      const data = await response.json();
      setSaveMessage(`Seeded ${data.reviews_created} demo review(s).`);
      await loadVault();
      await loadPortfolio();
      setActiveTab("Portfolio");
    } catch (err: any) {
      setError(err.message || "Could not seed demo reviews.");
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
        if (parsed.organization && parsed.items) setInput(JSON.stringify(parsed, null, 2));
        else if (Array.isArray(parsed)) {
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
        } else setInput(JSON.stringify(buildTextPayload(file.name, JSON.stringify(parsed)), null, 2));
      } else if (file.name.toLowerCase().endsWith(".csv")) setInput(JSON.stringify(parseCsvToPayload(file.name, text), null, 2));
      else setInput(JSON.stringify(buildTextPayload(file.name, text), null, 2));
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
      const response = await fetch(`${API_BASE}/api/reviews/analyze-save`, { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload) });
      if (!response.ok) throw new Error("Backend returned error: " + response.status);
      const data = await response.json();
      setResult(data);
      setCurrentReviewId(data.review_id || "");
      setRegisterRows(data.remediation_register || []);
      setActiveTab("Command Center");
      setSaveMessage("Review saved to vault.");
      await loadVault();
      await loadPortfolio();
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
      await loadPortfolio();
    } catch {
      setError("Could not delete review.");
    }
  }

  async function saveRegister() {
    if (!currentReviewId) {
      setSaveMessage("Run a saved review first.");
      return;
    }
    const response = await fetch(`${API_BASE}/api/reviews/${currentReviewId}/register`, { method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify({ rows: registerRows }) });
    if (response.ok) {
      setSaveMessage("Register saved to review vault.");
      await loadVault();
      await loadPortfolio();
    } else setSaveMessage("Register save failed.");
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
    a.download = "sentinel-v5-control-atlas-workspace.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadRegisterCsv() {
    const headers = ["Finding_ID","Severity","Risk_Domain","Control_Atlas_IDs","Affected_Item","Issue","Remediation","Evidence_Needed","Preferred_Artifacts","Owner","Target_Date","Status","Management_Response","Closure_Evidence","Validation_Notes"];
    const rows = registerRows.map((row) => [row.finding_id,row.severity,row.risk_domain,row.control_atlas_ids || "",row.affected_item,row.issue,row.remediation,row.evidence_needed,row.preferred_artifacts,row.owner,row.target_date,row.status,row.management_response,row.closure_evidence,row.validation_notes]);
    downloadCsv("sentinel-v5-control-atlas-register.csv", headers, rows);
  }

  function downloadControlAtlasCsv() {
    if (!result) return;
    const headers = ["Item","Domain","Control_ID","Control_Theme","Coverage","Rating","Missing_Evidence","Challenge_Questions"];
    const rows: any[][] = [];
    result.item_scorecards.forEach((item: any) => {
      (item.control_atlas_mapping?.mapped_controls || []).forEach((control: any) => {
        rows.push([item.item_title, item.domain, control.control_id, control.control_theme, control.control_coverage_score, control.control_rating, (control.missing_evidence || []).join("; "), (control.challenge_questions || []).join("; ")]);
      });
    });
    downloadCsv("sentinel-v5-control-atlas-mapping.csv", headers, rows);
  }

  function downloadPortfolioJson() {
    if (!portfolio) return;
    const blob = new Blob([JSON.stringify(portfolio, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v5-portfolio-snapshot.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function downloadHtmlReport() {
    if (!result) return;
    const endpoint = currentReviewId ? `${API_BASE}/api/reviews/${currentReviewId}/report-html` : `${API_BASE}/api/report-html`;
    const options = currentReviewId ? undefined : { method: "POST", headers: {"Content-Type": "application/json"}, body: input };
    const response = await fetch(endpoint, options as any);
    const reportHtml = await response.text();
    const blob = new Blob([reportHtml], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v5-control-atlas-report.html";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function downloadPortfolioReport() {
    const response = await fetch(`${API_BASE}/api/portfolio/report-html`);
    const reportHtml = await response.text();
    const blob = new Blob([reportHtml], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sentinel-v5-portfolio-control-atlas-report.html";
    a.click();
    URL.revokeObjectURL(url);
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
          <p className="eyebrow">Eye On Bits Pvt Ltd · Sentinel v5.0</p>
          <h1>Evidence Defensibility Workbench</h1>
          <p className="subtitle">
            Professional assurance workbench with review vault, portfolio analytics, control atlas mapping, challenge question bank, remediation register, and executive reporting.
          </p>
        </div>
        <div className="heroCard">
          <span>Major Upgrade</span>
          <strong>Control Atlas Mapper + Assurance Question Bank.</strong>
          <p>Sentinel now maps evidence to control themes, expected artifacts, missing control evidence, and examiner-style challenge questions.</p>
        </div>
      </section>

      <section className="caseLibrary">
        <div>
          <h2>Evidence Intake</h2>
          <p>Upload JSON, CSV, TXT, or MD evidence. Sentinel converts it into a structured review package and maps it to the Control Atlas.</p>
        </div>
        <div className="uploadBox">
          <input type="file" accept=".json,.csv,.txt,.md" onChange={handleFileUpload} />
          <span>v5.0 adds control objective coverage, missing control evidence, and challenge questions.</span>
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
          <p className="muted">Control Atlas mappings, scorecards, evidence requests, and persistent remediation register.</p>

          {!result && <div className="empty">Run a review, load one from the Review Vault, or seed demo reviews from Portfolio.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Defensibility</span><strong>{result.evidence_defensibility_score}/100</strong></div>
                <div className="scoreBox"><span>Control Atlas</span><strong>{result.control_atlas_coverage_score}/100</strong></div>
                <div className="scoreBox"><span>Metadata</span><strong>{result.metadata_completeness_score}/100</strong></div>
              </div>

              <div className="tabBar">
                {["Portfolio", "Command Center", "Control Atlas", "Output", "Findings"].map((tab) => (
                  <button key={tab} className={activeTab === tab ? "tab activeTab" : "tab"} onClick={() => setActiveTab(tab)}>{tab}</button>
                ))}
              </div>

              <div className="actions">
                <button onClick={saveRegister}>Save Register</button>
                <button onClick={downloadWorkspaceJson}>Workspace JSON</button>
                <button onClick={downloadRegisterCsv}>Register CSV</button>
                <button onClick={downloadControlAtlasCsv}>Control CSV</button>
                <button onClick={downloadHtmlReport}>HTML Report</button>
              </div>

              <div className="actions secondaryActions">
                <button onClick={copySummary}>Copy Executive Summary</button>
              </div>

              {activeTab === "Portfolio" && (
                <div>
                  <div className="summary">Portfolio Command Center summarizes saved evidence reviews, recurring domains, severity mix, remediation status, and Control Atlas concentration.</div>
                  <div className="actions">
                    <button onClick={loadPortfolio}>Refresh Portfolio</button>
                    <button onClick={seedDemoReviews}>Seed Demo Reviews</button>
                    <button onClick={downloadPortfolioJson}>Portfolio JSON</button>
                    <button onClick={downloadPortfolioReport}>Portfolio HTML</button>
                    <button onClick={loadVault}>Refresh Vault</button>
                  </div>
                  {!portfolio && <div className="empty">No portfolio snapshot loaded yet.</div>}
                  {portfolio && (
                    <div>
                      <div className="scoreRow">
                        <div className="scoreBox"><span>Saved Reviews</span><strong>{portfolio.total_reviews}</strong></div>
                        <div className="scoreBox"><span>Avg Defensibility</span><strong>{portfolio.average_defensibility_score}/100</strong></div>
                        <div className="scoreBox"><span>Open Items</span><strong>{portfolio.open_register_items}</strong></div>
                      </div>
                      <div className="miniGrid">
                        <div>
                          <h3>Control Atlas Concentration</h3>
                          {Object.entries(portfolio.control_atlas_distribution || {}).map(([k, v]: any) => (
                            <div key={k} className="miniRow"><span>{k}</span><strong>{v}</strong></div>
                          ))}
                        </div>
                        <div>
                          <h3>Risk Domain Distribution</h3>
                          {Object.entries(portfolio.risk_domain_distribution || {}).map(([k, v]: any) => (
                            <div key={k} className="miniRow"><span>{k}</span><strong>{v}</strong></div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

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
                      <h3>Review Snapshot</h3>
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
                          <span>Control Atlas: {row.control_atlas_ids || "Not mapped"}</span>
                        </div>
                        <p><b>Issue:</b> {row.issue}</p>
                        <p><b>Evidence needed:</b> {row.evidence_needed}</p>
                        <div className="registerGrid">
                          <label>Owner<input value={row.owner} onChange={(e) => updateRegisterRow(index, "owner", e.target.value)} /></label>
                          <label>Target Date<input type="date" value={row.target_date} onChange={(e) => updateRegisterRow(index, "target_date", e.target.value)} /></label>
                          <label>Status
                            <select value={row.status} onChange={(e) => updateRegisterRow(index, "status", e.target.value)}>
                              <option>Open</option><option>In Progress</option><option>Pending Evidence</option><option>Risk Accepted</option><option>Closed</option>
                            </select>
                          </label>
                        </div>
                        <label>Management Response<textarea className="smallText" value={row.management_response} onChange={(e) => updateRegisterRow(index, "management_response", e.target.value)} /></label>
                        <label>Closure Evidence<textarea className="smallText" value={row.closure_evidence} onChange={(e) => updateRegisterRow(index, "closure_evidence", e.target.value)} /></label>
                        <label>Validation Notes<textarea className="smallText" value={row.validation_notes} onChange={(e) => updateRegisterRow(index, "validation_notes", e.target.value)} /></label>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === "Control Atlas" && (
                <div className="nextSteps">
                  <h3>Control Atlas Mapping</h3>
                  {(result.item_scorecards || []).map((item: any) => (
                    <div key={item.item_title} className="scorecardItem">
                      <div className="scorecardTop">
                        <strong>{item.item_title}</strong>
                        <span>{item.control_atlas_mapping?.control_coverage_score}/100</span>
                      </div>
                      <p>{item.domain} · {item.artifact_profile?.artifact_type}</p>
                      {(item.control_atlas_mapping?.mapped_controls || []).map((control: any) => (
                        <div key={control.control_id} className="mappingBox">
                          <h4>{control.control_id} · {control.control_theme}</h4>
                          <p><b>Objective:</b> {control.control_objective}</p>
                          <p><b>Coverage:</b> {control.control_coverage_score}/100 · {control.control_rating}</p>
                          <p><b>Missing evidence:</b> {(control.missing_evidence || []).join(", ") || "None"}</p>
                          <p><b>Challenge questions:</b></p>
                          <ol>{(control.challenge_questions || []).map((q: string) => <li key={q}>{q}</li>)}</ol>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              )}

              {activeTab === "Output" && (
                <div>
                  <div className="summary">{result.executive_summary}</div>
                  <div className="miniGrid">
                    <div>
                      <h3>Severity Distribution</h3>
                      {Object.entries(result.severity_distribution || {}).map(([k, v]: any) => <div key={k} className="miniRow"><span>{k}</span><strong>{v}</strong></div>)}
                    </div>
                    <div>
                      <h3>Control Atlas Coverage</h3>
                      {(result.control_atlas_coverage || []).map((x: any) => <div key={x.control_id} className="miniRow"><span>{x.control_id}</span><strong>{x.finding_count}</strong></div>)}
                    </div>
                  </div>
                  <div className="nextSteps">
                    <h3>Recommended Next Steps</h3>
                    <ol>{(result.recommended_next_steps || []).map((step: string) => <li key={step}>{step}</li>)}</ol>
                  </div>
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
                      <p><b>Control Atlas:</b> {(finding.control_atlas_ids || []).join(", ")}</p>
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
