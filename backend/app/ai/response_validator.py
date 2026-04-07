from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

DISCLAIMER = (
    "This is a statistical estimate based on resume–JD pattern matching. "
    "It does not represent recruiter judgment or guarantee any hiring outcome."
)
DEFAULT_OLLAMA_MODEL = "gemma:2b"

TOP_LEVEL_KEYS = [
    "meta",
    "candidate_profile",
    "ats_analysis",
    "job_analysis",
    "match_analysis",
    "project_analysis",
    "shortlist_estimation",
    "improvement_plan",
    "final_verdict",
]

ARRAY_PATHS = [
    ("candidate_profile", "education"),
    ("candidate_profile", "skills_detected"),
    ("candidate_profile", "certifications"),
    ("ats_analysis", "issues"),
    ("job_analysis", "required_skills"),
    ("job_analysis", "preferred_skills"),
    ("job_analysis", "key_responsibilities"),
    ("job_analysis", "certifications_required"),
    ("match_analysis", "skills_match", "matched_skills"),
    ("match_analysis", "skills_match", "missing_required_skills"),
    ("match_analysis", "skills_match", "missing_preferred_skills"),
    ("match_analysis", "skills_match", "extra_skills_not_in_jd"),
    ("match_analysis", "keyword_coverage", "important_keywords_present"),
    ("match_analysis", "keyword_coverage", "important_keywords_missing"),
    ("project_analysis", "projects"),
    ("shortlist_estimation", "positive_signals"),
    ("shortlist_estimation", "negative_signals"),
    ("improvement_plan", "priority_actions"),
    ("improvement_plan", "keywords_to_add"),
    ("improvement_plan", "skills_to_highlight"),
    ("improvement_plan", "sections_to_improve"),
    ("final_verdict", "top_strengths"),
    ("final_verdict", "critical_gaps"),
    ("final_verdict", "recommended_next_steps"),
]

SCORE_PATHS = [
    ("ats_analysis", "ats_score"),
    ("ats_analysis", "keyword_density_score"),
    ("ats_analysis", "formatting_score"),
    ("ats_analysis", "section_structure_score"),
    ("match_analysis", "overall_match_score"),
    ("match_analysis", "skills_match", "score"),
    ("match_analysis", "experience_alignment", "score"),
    ("match_analysis", "education_alignment", "score"),
    ("match_analysis", "domain_alignment", "score"),
    ("match_analysis", "keyword_coverage", "score"),
    ("project_analysis", "overall_project_relevance_score"),
    ("shortlist_estimation", "probability_range_low"),
    ("shortlist_estimation", "probability_range_high"),
    ("final_verdict", "overall_score"),
]

PROJECT_SCORE_PATH = ("project_analysis", "projects")


def _default_response_with_error(message: str) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "meta": {
            "analysis_id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "model_used": os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL),
            "incomplete": True,
        },
        "candidate_profile": {
            "name": None,
            "email": None,
            "phone": None,
            "detected_domain": "",
            "detected_seniority_level": "unclear",
            "total_experience_years": None,
            "education": [],
            "skills_detected": [],
            "certifications": [],
        },
        "ats_analysis": {
            "ats_score": 0,
            "ats_grade": "Poor",
            "is_ats_friendly": False,
            "issues": [],
            "keyword_density_score": 0,
            "formatting_score": 0,
            "section_structure_score": 0,
        },
        "job_analysis": {
            "job_title_detected": "",
            "domain": "",
            "seniority_level": "entry",
            "required_skills": [],
            "preferred_skills": [],
            "required_experience_years": None,
            "key_responsibilities": [],
            "certifications_required": [],
        },
        "match_analysis": {
            "overall_match_score": 0,
            "skills_match": {
                "score": 0,
                "matched_skills": [],
                "missing_required_skills": [],
                "missing_preferred_skills": [],
                "extra_skills_not_in_jd": [],
            },
            "experience_alignment": {"score": 0, "explanation": ""},
            "education_alignment": {"score": 0, "explanation": ""},
            "domain_alignment": {"score": 0, "is_same_domain": False, "explanation": ""},
            "keyword_coverage": {"score": 0, "important_keywords_present": [], "important_keywords_missing": []},
        },
        "project_analysis": {
            "projects_found": 0,
            "projects": [],
            "overall_project_relevance_score": 0,
        },
        "shortlist_estimation": {
            "probability_range_low": 0,
            "probability_range_high": 0,
            "probability_label": "0–0%",
            "confidence": "low",
            "disclaimer": DISCLAIMER,
            "positive_signals": [],
            "negative_signals": [],
            "explanation": "",
        },
        "improvement_plan": {
            "priority_actions": [],
            "keywords_to_add": [],
            "skills_to_highlight": [],
            "sections_to_improve": [],
        },
        "final_verdict": {
            "overall_score": 0,
            "overall_grade": "Poor",
            "summary": f"Analysis response could not be parsed completely. {message}",
            "top_strengths": [],
            "critical_gaps": ["AI response parsing failed"],
            "recommended_next_steps": ["Retry analysis with a clearer resume and job description"],
        },
    }


def _strip_code_fences(raw: str) -> str:
    value = raw.strip()
    fence_match = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", value, re.I)
    if fence_match:
        return fence_match.group(1).strip()
    return value


def _ensure_path_dict(container: dict[str, Any], key: str) -> dict[str, Any]:
    if key not in container or not isinstance(container[key], dict):
        container[key] = {}
    return container[key]


def _set_default_list(data: dict[str, Any], path: tuple[str, ...]) -> None:
    cursor: dict[str, Any] = data
    for key in path[:-1]:
        cursor = _ensure_path_dict(cursor, key)
    leaf = path[-1]
    if leaf not in cursor or not isinstance(cursor[leaf], list):
        cursor[leaf] = []


def _clamp_int(value: Any) -> int:
    try:
        numeric = int(round(float(value)))
    except Exception:
        numeric = 0
    return max(0, min(100, numeric))


def _set_clamped_score(data: dict[str, Any], path: tuple[str, ...]) -> None:
    cursor: dict[str, Any] = data
    for key in path[:-1]:
        cursor = _ensure_path_dict(cursor, key)
    leaf = path[-1]
    cursor[leaf] = _clamp_int(cursor.get(leaf, 0))


def validate_and_normalize_response(raw_response_text: str) -> dict[str, Any]:
    cleaned = _strip_code_fences(raw_response_text)
    try:
        data = json.loads(cleaned)
    except Exception as exc:
        return _default_response_with_error(str(exc))

    if not isinstance(data, dict):
        return _default_response_with_error("Top-level response is not a JSON object.")

    missing_or_malformed = False
    for key in TOP_LEVEL_KEYS:
        if key not in data or not isinstance(data[key], dict):
            data[key] = {}
            missing_or_malformed = True

    for path in ARRAY_PATHS:
        _set_default_list(data, path)

    for path in SCORE_PATHS:
        _set_clamped_score(data, path)

    projects = data.get(PROJECT_SCORE_PATH[0], {}).get(PROJECT_SCORE_PATH[1], [])
    if isinstance(projects, list):
        for item in projects:
            if isinstance(item, dict):
                item["relevance_score"] = _clamp_int(item.get("relevance_score", 0))

    meta = data["meta"]
    if not isinstance(meta.get("analysis_id"), str) or not meta.get("analysis_id"):
        meta["analysis_id"] = str(uuid.uuid4())
        missing_or_malformed = True
    if not isinstance(meta.get("timestamp"), str) or not meta.get("timestamp"):
        meta["timestamp"] = datetime.now(timezone.utc).isoformat()
        missing_or_malformed = True
    if not isinstance(meta.get("model_used"), str) or not meta.get("model_used"):
        meta["model_used"] = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    meta["incomplete"] = bool(meta.get("incomplete", False) or missing_or_malformed)

    shortlist = data["shortlist_estimation"]
    if not isinstance(shortlist.get("disclaimer"), str) or not shortlist.get("disclaimer").strip():
        shortlist["disclaimer"] = DISCLAIMER

    low = _clamp_int(shortlist.get("probability_range_low", 0))
    high = _clamp_int(shortlist.get("probability_range_high", 0))
    if high < low:
        low, high = high, low
    shortlist["probability_range_low"] = low
    shortlist["probability_range_high"] = high
    if not isinstance(shortlist.get("probability_label"), str) or not shortlist.get("probability_label").strip():
        shortlist["probability_label"] = f"{low}–{high}%"

    final_verdict = data["final_verdict"]
    if not isinstance(final_verdict.get("summary"), str):
        final_verdict["summary"] = ""

    return data
