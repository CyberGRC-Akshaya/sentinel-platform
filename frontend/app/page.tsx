"use client";

import { useEffect, useState } from "react";

const defaultPayload = {
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
    },
    {
      title: "Vendor SOC 2 Evidence",
      content: "Vendor provided SOC 2 Type II report. Vendor processes customer data and NPI. Evidence does not include data flow, retention description, or CUEC analysis.",
      source_system: "Vendor Portal",
      owner: "TPRM",
      reporting_period: "Annual Review"
    }
  ]
};

type SampleCase = {
  id: string;
  label: string;
  description: string;
  payload: any;
};

export default function Home() {
  const [input, setInput] = useState(JSON.stringify(defaultPayload, null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [samples, setSamples] = useState<SampleCase[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/sample-cases")
      .then((res) => res.json())
      .then((data) => setSamples(data.cases || []))
      .catch(() => setSamples([]));
  }, []);

  function loadSample(sample: SampleCase) {
    setInput(JSON.stringify(sample.payload, null, 2));
    setResult(null);
    setError("");
  }

  async function analyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = JSON.parse(input);
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Backend returned error: " + response.status);

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function downloadReport() {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const stamp = new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-");
    link.href = url;
    link.download = `sentinel-examiner-report-${stamp}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  async function copyExecutiveSummary() {
    if (!result) return;
    const text = [
      "Sentinel Examiner Summary",
      `Organization: ${result.organization}`,
      `Evidence Type: ${result.evidence_type}`,
      `Rating: ${result.overall_rating}`,
      `Assurance Score: ${result.assurance_score}/100`,
      `Findings: ${result.total_findings}`,
      "",
      result.executive_summary,
      "",
      result.executive_posture
    ].join("\n");
    await navigator.clipboard.writeText(text);
    alert("Executive summary copied.");
  }

  const severityOrder = ["Critical", "High", "Medium", "Low"];

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Eye On Bits Pvt Ltd</p>
          <h1>Sentinel Assurance Platform</h1>
          <p className="subtitle">
            AI-native examiner intelligence for metrics validation, evidence challenge,
            control assurance, and regulatory-ready governance review.
          </p>
        </div>
        <div className="heroCard">
          <span>Sentinel v0.2</span>
          <strong>Examiner Intelligence Console</strong>
          <p>Built for BFSI, audit, GRC, privacy, TPRM, AI governance, and SDLC assurance workflows.</p>
        </div>
      </section>

      <section className="sampleStrip">
        <div>
          <h2>Sample Case Library</h2>
          <p>Load realistic regulated-industry evidence packages and run examiner review.</p>
        </div>
        <div className="sampleButtons">
          {samples.map((sample) => (
            <button className="sampleBtn" key={sample.id} onClick={() => loadSample(sample)}>
              <strong>{sample.label}</strong>
              <span>{sample.description}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Evidence Input</h2>
          <p className="muted">Paste or load evidence package JSON. Sentinel will challenge evidence quality, metric logic, and governance defensibility.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button className="primaryBtn" onClick={analyze} disabled={loading}>{loading ? "Running Examiner Review..." : "Run Examiner Review"}</button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="panel outputPanel">
          <div className="panelHeader">
            <div>
              <h2>Examiner Output</h2>
              <p className="muted">Executive-ready findings, evidence gaps, challenge questions, and remediation guidance.</p>
            </div>
            {result && (
              <div className="actions">
                <button onClick={downloadReport}>Download JSON</button>
                <button onClick={copyExecutiveSummary}>Copy Summary</button>
                <button onClick={() => window.print()}>Print</button>
              </div>
            )}
          </div>

          {!result && <div className="empty">Run the examiner review to generate assurance score, findings, challenge questions, and remediation guidance.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Assurance Score</span><strong>{result.assurance_score}/100</strong></div>
                <div className="scoreBox"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                <div className="scoreBox"><span>Findings</span><strong>{result.total_findings}</strong></div>
                <div className="scoreBox"><span>High Risk</span><strong>{result.high_risk_findings}</strong></div>
              </div>

              <div className="summary"><b>Executive Summary:</b> {result.executive_summary}<br /><br /><b>Executive Posture:</b> {result.executive_posture}</div>

              <div className="miniGrid">
                <div className="miniPanel">
                  <h3>Severity Distribution</h3>
                  <div className="bars">
                    {severityOrder.map((sev) => {
                      const count = result.severity_counts?.[sev] || 0;
                      return (
                        <div className="barRow" key={sev}>
                          <span>{sev}</span>
                          <div className="barTrack"><div className={`barFill ${sev.toLowerCase()}`} style={{ width: `${Math.min(100, count * 24)}%` }} /></div>
                          <b>{count}</b>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="miniPanel">
                  <h3>Top Risk Domains</h3>
                  {result.top_domains?.map((domain: any) => (
                    <div className="domainRow" key={domain.domain}><span>{domain.domain}</span><b>{domain.count}</b></div>
                  ))}
                </div>
              </div>

              <div className="nextSteps">
                <h3>Recommended Next Steps</h3>
                <ol>{result.recommended_next_steps.map((step: string) => <li key={step}>{step}</li>)}</ol>
              </div>

              <div className="findings">
                {result.findings.map((finding: any, index: number) => (
                  <div key={index} className="finding">
                    <div className="findingTop">
                      <div><h3>{finding.title}</h3><span className="domainTag">{finding.domain}</span></div>
                      <span className={"badge " + finding.severity.toLowerCase()}>{finding.severity}</span>
                    </div>
                    <p><b>Affected item:</b> {finding.affected_item}</p>
                    <p><b>Issue:</b> {finding.issue}</p>
                    <p><b>Evidence gap:</b> {finding.evidence_gap}</p>
                    <p><b>Examiner question:</b> {finding.examiner_question}</p>
                    <p><b>Remediation:</b> {finding.remediation}</p>
                    <p><b>Buyer value:</b> {finding.buyer_value}</p>
                    <div className="frameworks">{finding.framework_relevance.map((fw: string) => <span key={fw}>{fw}</span>)}</div>
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