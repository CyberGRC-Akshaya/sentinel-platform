# Sentinel Stage 4 Backend AI Service Installer
# Adds optional, fallback-safe AI assist backend service and route.
# No frontend changes.

$ErrorActionPreference = "Stop"

Write-Host "=== Sentinel Stage 4 Backend AI Service Installer ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "You are not in the expected project folder." -ForegroundColor Red
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$mainPath = Join-Path $project "backend\app\main.py"
$serviceDir = Join-Path $project "backend\app\services"
$aiPath = Join-Path $serviceDir "ai_review.py"
$requirementsPath = Join-Path $project "backend\requirements.txt"
$envExamplePath = Join-Path $project ".env.example"

if (!(Test-Path $mainPath)) {
    Write-Host "backend/app/main.py not found." -ForegroundColor Red
    exit 1
}

$raw = Get-Content $mainPath -Raw

if ($raw.Contains("/api/ai/assist-review")) {
    Write-Host "AI assist route already appears to exist. No changes made." -ForegroundColor Yellow
    exit 0
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = Join-Path $project "backend\app\main.py.stage4-ai-backup-$timestamp"
Copy-Item $mainPath $backupPath -Force
Write-Host "Backup created:" -ForegroundColor Green
Write-Host $backupPath

New-Item -ItemType Directory -Path $serviceDir -Force | Out-Null

$aiService = @'
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AIReviewRequest(BaseModel):
    review_id: Optional[str] = None
    mode: str = "executive_summary"
    organization: Optional[str] = None
    industry: Optional[str] = None
    review_objective: Optional[str] = None
    result: Dict[str, Any]
    findings: Optional[List[Dict[str, Any]]] = None


def ai_enabled() -> bool:
    return os.getenv("AI_REVIEW_ENABLED", "false").strip().lower() in {"1", "true", "yes", "on"}


def ai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-5.5")


def build_ai_prompt(request: AIReviewRequest) -> str:
    result = request.result or {}
    findings = request.findings or result.get("findings", []) or []
    trimmed_findings = findings[:8]

    return f"""
You are Sentinel's evidence defensibility review assistant.

You do not make final audit conclusions.
You do not override Sentinel's deterministic scores.
You do not invent evidence.
You produce reviewer-ready drafting support for human review.

Context:
- Organization: {request.organization or result.get("organization", "Not provided")}
- Industry: {request.industry or result.get("industry", "Not provided")}
- Review objective: {request.review_objective or result.get("review_objective", "Not provided")}
- Requested mode: {request.mode}

Sentinel deterministic result:
- Evidence defensibility score: {result.get("evidence_defensibility_score", "Not available")}
- Rating: {result.get("overall_rating", result.get("rating", "Not available"))}
- Control Atlas coverage: {result.get("control_atlas_coverage_score", "Not available")}
- Metadata completeness: {result.get("metadata_completeness_score", "Not available")}
- Total findings: {result.get("total_findings", len(findings))}

Findings excerpt:
{trimmed_findings}

Return a concise professional response with these sections:
1. Executive Summary
2. Key Evidence Gaps
3. Suggested Evidence Requests
4. Reviewer Challenge Questions
5. Management-Ready Next Steps
6. Human Review Note
""".strip()


def fallback_response(request: AIReviewRequest, reason: str) -> Dict[str, Any]:
    result = request.result or {}
    findings = request.findings or result.get("findings", []) or []
    return {
        "ai_enabled": False,
        "status": "fallback",
        "reason": reason,
        "model": ai_model(),
        "timestamp": datetime.utcnow().isoformat(),
        "mode": request.mode,
        "human_review_required": True,
        "output": {
            "executive_summary": (
                "AI assist is not active. Sentinel's deterministic rule engine remains available. "
                f"The review result is rated '{result.get('overall_rating', result.get('rating', 'Not available'))}' "
                f"with {result.get('total_findings', len(findings))} finding(s)."
            ),
            "suggested_next_steps": [
                "Review deterministic findings.",
                "Validate missing evidence with the evidence owner.",
                "Use exported register and HTML report for follow-up.",
            ],
            "human_review_note": "This fallback was generated without calling an AI model."
        },
        "prompt_log": {
            "review_id": request.review_id,
            "mode": request.mode,
            "model": ai_model(),
            "called_model": False,
            "input_summary": {
                "score": result.get("evidence_defensibility_score"),
                "rating": result.get("overall_rating", result.get("rating")),
                "findings_count": result.get("total_findings", len(findings)),
            }
        }
    }


def generate_ai_assist(request: AIReviewRequest) -> Dict[str, Any]:
    if not ai_enabled():
        return fallback_response(request, "AI_REVIEW_ENABLED is not true.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return fallback_response(request, "OPENAI_API_KEY is not configured.")

    try:
        from openai import OpenAI
    except Exception as exc:
        return fallback_response(request, f"OpenAI Python package is not available: {exc}")

    prompt = build_ai_prompt(request)

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=ai_model(),
            instructions=(
                "You are an evidence defensibility review assistant. "
                "You support human reviewers. Do not make final audit conclusions, "
                "do not invent facts, and do not override deterministic Sentinel scores."
            ),
            input=prompt,
        )

        return {
            "ai_enabled": True,
            "status": "completed",
            "model": ai_model(),
            "timestamp": datetime.utcnow().isoformat(),
            "mode": request.mode,
            "human_review_required": True,
            "output": {
                "text": getattr(response, "output_text", str(response))
            },
            "prompt_log": {
                "review_id": request.review_id,
                "mode": request.mode,
                "model": ai_model(),
                "called_model": True,
                "input_summary": {
                    "prompt_chars": len(prompt),
                    "result_keys": sorted(list((request.result or {}).keys()))[:30],
                }
            }
        }
    except Exception as exc:
        return fallback_response(request, f"AI call failed safely: {exc}")
'@

Set-Content -Path $aiPath -Value $aiService -Encoding UTF8

# Add import to main.py
$importLine = "from app.services.ai_review import AIReviewRequest, generate_ai_assist`n"
if ($raw.Contains("from app.services.scoring import")) {
    $updated = $raw
    if ($updated.Contains("from app.services.scoring import (`r`n")) {
        $updated = $updated.Replace("from app.services.scoring import (`r`n", $importLine + "from app.services.scoring import (`r`n")
    } elseif ($updated.Contains("from app.services.scoring import (`n")) {
        $updated = $updated.Replace("from app.services.scoring import (`n", $importLine + "from app.services.scoring import (`n")
    } else {
        $updated = $importLine + $updated
    }
} else {
    $updated = $importLine + $raw
}

$routeBlock = @'

@app.post("/api/ai/assist-review")
def ai_assist_review(request: AIReviewRequest):
    return generate_ai_assist(request)

'@

$marker = '@app.post("/api/reviews/analyze-save")'
$markerIndex = $updated.IndexOf($marker)

if ($markerIndex -lt 0) {
    Write-Host "Could not find route insertion marker. Restoring backup." -ForegroundColor Red
    Copy-Item $backupPath $mainPath -Force
    Remove-Item $aiPath -Force
    exit 1
}

$updated = $updated.Insert($markerIndex, $routeBlock)
Set-Content -Path $mainPath -Value $updated -Encoding UTF8

# Requirements: add openai if not present
if (Test-Path $requirementsPath) {
    $reqRaw = Get-Content $requirementsPath -Raw
    if ($reqRaw -notmatch "(?im)^openai(\s|=|>|<|$)") {
        Add-Content -Path $requirementsPath -Value "openai" -Encoding UTF8
    }
} else {
    Set-Content -Path $requirementsPath -Value "fastapi`nuvicorn`nopenai`n" -Encoding UTF8
}

# .env.example: add safe config only, never real secret
$envBlock = @"

# Sentinel Stage 4 AI Assist
# Do not commit real API keys.
AI_REVIEW_ENABLED=false
OPENAI_MODEL=gpt-5.5
OPENAI_API_KEY=
"@

if (Test-Path $envExamplePath) {
    $envRaw = Get-Content $envExamplePath -Raw
    if ($envRaw -notmatch "AI_REVIEW_ENABLED") {
        Add-Content -Path $envExamplePath -Value $envBlock -Encoding UTF8
    }
} else {
    Set-Content -Path $envExamplePath -Value $envBlock.TrimStart() -Encoding UTF8
}

Write-Host "Created:" -ForegroundColor Green
Write-Host $aiPath
Write-Host "Updated:" -ForegroundColor Green
Write-Host $mainPath
Write-Host $requirementsPath
Write-Host $envExamplePath

Write-Host "`nSyntax check:" -ForegroundColor Cyan
try {
    python -m py_compile backend\app\main.py backend\app\services\ai_review.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python syntax check passed." -ForegroundColor Green
    } else {
        Write-Host "Python syntax check failed. Review output above." -ForegroundColor Red
    }
} catch {
    Write-Host "Python command unavailable or failed. Docker build will validate." -ForegroundColor Yellow
}

Write-Host "`nNext test:" -ForegroundColor Cyan
Write-Host "docker compose down --remove-orphans"
Write-Host "docker compose up --build"
Write-Host "Then test POST http://localhost:8000/api/ai/assist-review"
