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
