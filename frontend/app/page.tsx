"use client";

import { useState } from "react";

const samplePayload = {
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

export default function Home() {
  const [input, setInput] = useState(JSON.stringify(samplePayload, null, 2));
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

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
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    }
  }

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
          <span>Sentinel v0.1</span>
          <strong>Metrics & Evidence Examiner</strong>
          <p>Designed for BFSI, audit, GRC, privacy, TPRM, and SDLC assurance workflows.</p>
        </div>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Evidence Input</h2>
          <p className="muted">Paste evidence package JSON below. The sample is already loaded.</p>
          <textarea value={input} onChange={(e) => setInput(e.target.value)} />
          <button onClick={analyze}>Run Examiner Review</button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="panel">
          <h2>Examiner Output</h2>
          {!result && <div className="empty">Run the examiner review to generate assurance score, findings, challenge questions, and remediation guidance.</div>}

          {result && (
            <div>
              <div className="scoreRow">
                <div className="scoreBox"><span>Assurance Score</span><strong>{result.assurance_score}/100</strong></div>
                <div className="scoreBox"><span>Rating</span><strong>{result.overall_rating}</strong></div>
                <div className="scoreBox"><span>Findings</span><strong>{result.total_findings}</strong></div>
              </div>

              <div className="summary">{result.executive_summary}</div>

              <div className="findings">
                {result.findings.map((finding: any, index: number) => (
                  <div key={index} className="finding">
                    <div className="findingTop">
                      <h3>{finding.title}</h3>
                      <span className={"badge " + finding.severity.toLowerCase()}>{finding.severity}</span>
                    </div>
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
