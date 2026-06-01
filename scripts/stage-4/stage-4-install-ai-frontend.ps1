# Sentinel Stage 4 AI Frontend Integration Installer
# Adds AI Assist button + output panel to frontend/app/page.tsx.
# No backend changes.

$ErrorActionPreference = "Stop"

Write-Host "=== Sentinel Stage 4 AI Frontend Integration Installer ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "You are not in expected project folder." -ForegroundColor Red
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$pagePath = Join-Path $project "frontend\app\page.tsx"
$cssPath = Join-Path $project "frontend\app\globals.css"

if (!(Test-Path $pagePath)) {
    Write-Host "page.tsx not found." -ForegroundColor Red
    exit 1
}

$raw = Get-Content $pagePath -Raw

if ($raw.Contains("runAiAssist")) {
    Write-Host "AI frontend integration already appears to exist. No changes made." -ForegroundColor Yellow
    exit 0
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = Join-Path $project "frontend\app\page.tsx.stage4-ai-frontend-backup-$timestamp"
Copy-Item $pagePath $backupPath -Force
Write-Host "Backup created:" -ForegroundColor Green
Write-Host $backupPath

# 1. Add AI states after finalRelease state.
$stateMarker = '  const [finalRelease, setFinalRelease] = useState<any>(null);'
$stateInsert = @'
  const [finalRelease, setFinalRelease] = useState<any>(null);
  const [aiAssist, setAiAssist] = useState<any>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");
'@

if (!$raw.Contains($stateMarker)) {
    Write-Host "Could not find state marker." -ForegroundColor Red
    exit 1
}
$updated = $raw.Replace($stateMarker, $stateInsert)

# 2. Clear AI assist when running new analysis.
$analyzeMarker = '    setSaveMessage("");'
$analyzeInsert = @'
    setSaveMessage("");
    setAiAssist(null);
    setAiError("");
'@
$analyzeIndex = $updated.IndexOf($analyzeMarker)
if ($analyzeIndex -ge 0) {
    $updated = $updated.Substring(0, $analyzeIndex) + $analyzeInsert + $updated.Substring($analyzeIndex + $analyzeMarker.Length)
} else {
    Write-Host "Could not find analyze marker." -ForegroundColor Red
    Copy-Item $backupPath $pagePath -Force
    exit 1
}

# 3. Clear AI assist when loading saved review.
$loadMarkerLf = "  async function loadSavedReview(reviewId: string) {`n    setError(`"`");"
$loadMarkerCrLf = "  async function loadSavedReview(reviewId: string) {`r`n    setError(`"`");"
$loadInsertCrLf = "  async function loadSavedReview(reviewId: string) {`r`n    setError(`"`");`r`n    setAiAssist(null);`r`n    setAiError(`"`");"

if ($updated.Contains($loadMarkerCrLf)) {
    $updated = $updated.Replace($loadMarkerCrLf, $loadInsertCrLf)
} elseif ($updated.Contains($loadMarkerLf)) {
    $updated = $updated.Replace($loadMarkerLf, $loadInsertCrLf)
} else {
    Write-Host "Warning: could not insert AI clear lines into loadSavedReview. Continuing." -ForegroundColor Yellow
}

# 4. Insert AI functions before copySummary.
$functionMarker = '  async function copySummary() {'
$aiFunctions = @'
  async function runAiAssist() {
    if (!result) {
      setSaveMessage("Run or load a saved review before using AI Assist.");
      return;
    }

    setAiLoading(true);
    setAiError("");
    setAiAssist(null);

    let parsedInput: any = {};
    try {
      parsedInput = JSON.parse(input);
    } catch {
      parsedInput = {};
    }

    try {
      const response = await fetch(`${API_BASE}/api/ai/assist-review`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          review_id: currentReviewId || "",
          mode: "executive_summary",
          organization: result.organization || parsedInput.organization || "",
          industry: result.industry || parsedInput.industry || "",
          review_objective: result.review_objective || parsedInput.review_objective || "",
          result: { ...result, remediation_register: registerRows },
          findings: result.findings || registerRows || []
        })
      });

      if (!response.ok) throw new Error("AI Assist endpoint returned error: " + response.status);

      const data = await response.json();
      setAiAssist(data);
      setSaveMessage(data.status === "fallback" ? "AI Assist fallback generated safely." : "AI Assist draft generated.");
    } catch (err: any) {
      setAiError(err.message || "AI Assist failed safely.");
    } finally {
      setAiLoading(false);
    }
  }

  function aiAssistDisplayText() {
    if (!aiAssist) return "";
    if (aiAssist.output?.text) return aiAssist.output.text;

    const parts: string[] = [];
    if (aiAssist.output?.executive_summary) parts.push(aiAssist.output.executive_summary);
    if (Array.isArray(aiAssist.output?.suggested_next_steps)) {
      parts.push("Suggested Next Steps:\n" + aiAssist.output.suggested_next_steps.map((x: string, index: number) => `${index + 1}. ${x}`).join("\n"));
    }
    if (aiAssist.output?.human_review_note) parts.push("Human Review Note:\n" + aiAssist.output.human_review_note);

    return parts.join("\n\n") || "AI Assist returned no displayable text.";
  }

'@

if (!$updated.Contains($functionMarker)) {
    Write-Host "Could not find copySummary function marker." -ForegroundColor Red
    Copy-Item $backupPath $pagePath -Force
    exit 1
}
$updated = $updated.Replace($functionMarker, $aiFunctions + $functionMarker)

# 5. Replace secondary actions block with AI Assist button and output panel.
$oldActions = @'
              <div className="actions secondaryActions">
                <button onClick={copySummary}>Copy Executive Summary</button>
              </div>
'@

$newActions = @'
              <div className="actions secondaryActions">
                <button onClick={copySummary}>Copy Executive Summary</button>
                <button onClick={runAiAssist} disabled={aiLoading}>{aiLoading ? "AI Assist Running..." : "AI Assist Review"}</button>
              </div>

              {aiError && <div className="error">{aiError}</div>}

              {aiAssist && (
                <div className="aiAssistPanel">
                  <div className="scorecardTop">
                    <strong>AI-Assisted Review Draft</strong>
                    <span>{aiAssist.status} · {aiAssist.model}</span>
                  </div>
                  <p className="muted">
                    Drafting support only. Sentinel scores remain deterministic and human review is required before audit, management, or client use.
                  </p>
                  <pre className="aiAssistText">{aiAssistDisplayText()}</pre>
                  <div className="miniGrid">
                    <div className="miniRow"><span>AI Status</span><strong>{aiAssist.status}</strong></div>
                    <div className="miniRow"><span>Human Review</span><strong>Required</strong></div>
                    <div className="miniRow"><span>Mode</span><strong>{aiAssist.mode}</strong></div>
                  </div>
                </div>
              )}
'@

if (!$updated.Contains($oldActions)) {
    Write-Host "Could not find secondary actions block." -ForegroundColor Red
    Copy-Item $backupPath $pagePath -Force
    exit 1
}
$updated = $updated.Replace($oldActions, $newActions)

Set-Content -Path $pagePath -Value $updated -Encoding UTF8

# 6. Append CSS polish for AI panel if not already present.
$css = Get-Content $cssPath -Raw
if (!$css.Contains("Sentinel Stage 4 AI Assist UI")) {
    $cssBlock = @'

/* =========================================================
   Sentinel Stage 4 AI Assist UI
   Scope: AI assist panel only.
   ========================================================= */

.aiAssistPanel {
  margin: 18px 0 22px;
  padding: 18px;
  border: 1px solid rgba(56, 189, 248, 0.26);
  border-radius: var(--sentinel-radius-lg, 24px);
  background:
    radial-gradient(circle at top left, rgba(56, 189, 248, 0.14), transparent 32%),
    linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(2, 6, 23, 0.72));
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
}

.aiAssistPanel .scorecardTop span {
  color: var(--sentinel-accent, #38bdf8);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.aiAssistText {
  white-space: pre-wrap;
  margin: 14px 0;
  padding: 16px;
  max-height: 420px;
  overflow: auto;
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(2, 6, 23, 0.72);
  color: #e2e8f0;
  font-family: "Cascadia Code", "Consolas", "SFMono-Regular", monospace;
  font-size: 0.88rem;
  line-height: 1.58;
}
'@
    Add-Content -Path $cssPath -Value $cssBlock -Encoding UTF8
}

Write-Host "Updated:" -ForegroundColor Green
Write-Host $pagePath
Write-Host $cssPath

Write-Host "`nNext:" -ForegroundColor Cyan
Write-Host "docker compose down --remove-orphans"
Write-Host "docker compose up --build"

