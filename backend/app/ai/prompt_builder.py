from __future__ import annotations

import json
from typing import Any

JSON_TEMPLATE = {
    "meta": {"analysis_id": "", "timestamp": "", "model_used": "", "incomplete": False},
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
    "project_analysis": {"projects_found": 0, "projects": [], "overall_project_relevance_score": 0},
    "shortlist_estimation": {
        "probability_range_low": 0,
        "probability_range_high": 0,
        "probability_label": "0–0%",
        "confidence": "low",
        "disclaimer": "This is a statistical estimate based on resume–JD pattern matching. It does not represent recruiter judgment or guarantee any hiring outcome.",
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
        "summary": "",
        "top_strengths": [],
        "critical_gaps": [],
        "recommended_next_steps": [],
    },
}

OUTPUT_INSTRUCTION = "Return only one JSON object."


def _truncate_text(text: str, max_chars: int) -> str:
    normalized = (text or "").strip()
    if len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars]


def build_prompts(resume_data: dict[str, Any], jd_data: dict[str, Any], jd_text: str) -> dict[str, str]:
    truncated_resume = _truncate_text(str(resume_data.get("raw_text", "")), 7000)
    truncated_jd = _truncate_text(jd_text, 2000)

    system_prompt = (
        "You are a strict JSON API for ML Intern resume analysis.\n"
        "Target role: Machine Learning Intern.\n"
        "Score 0-100 integers only.\n"
        "Keep suggestions concise and practical.\n"
        "Do not output markdown or explanations outside JSON.\n"
        "Use this exact JSON shape and keys:\n"
        f"{json.dumps(JSON_TEMPLATE, ensure_ascii=False, separators=(',', ':'))}"
    )

    user_payload = {
        "resume_sections": resume_data.get("sections", {}),
        "resume_ats_flags": resume_data.get("ats_flags", []),
        "resume_word_count": resume_data.get("word_count", 0),
        "job_analysis_seed": jd_data,
    }

    user_prompt = (
        "RESUME:\n"
        f"{truncated_resume}\n\n"
        "JOB_DESCRIPTION:\n"
        f"{truncated_jd}\n\n"
        "PARSED_CONTEXT:\n"
        f"{json.dumps(user_payload, ensure_ascii=False, separators=(',', ':'))}\n\n"
        f"{OUTPUT_INSTRUCTION}"
    )

    return {"system_prompt": system_prompt, "user_prompt": user_prompt}
