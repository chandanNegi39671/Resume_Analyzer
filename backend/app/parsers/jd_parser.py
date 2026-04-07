from __future__ import annotations

import re
from typing import Any


SKILL_KEYWORDS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "node",
    "fastapi",
    "django",
    "flask",
    "spring",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "git",
    "ci/cd",
    "graphql",
    "rest",
    "microservices",
    "linux",
]

CERTIFICATION_PATTERNS = [
    "aws certified",
    "azure certification",
    "google professional",
    "pmp",
    "scrum master",
    "ckad",
    "cka",
]

DOMAIN_KEYWORDS = {
    "data": ["data", "machine learning", "analytics", "ai", "nlp"],
    "backend": ["backend", "api", "microservice", "server-side", "distributed systems"],
    "frontend": ["frontend", "react", "ui", "ux", "web"],
    "devops": ["devops", "infrastructure", "kubernetes", "terraform", "ci/cd"],
    "mobile": ["android", "ios", "flutter", "react native", "mobile"],
    "security": ["security", "cybersecurity", "penetration", "iam", "threat"],
}


def _extract_job_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title_patterns = [
        re.compile(r"^\s*job\s*title\s*:\s*(.+)$", re.I),
        re.compile(r"^\s*position\s*:\s*(.+)$", re.I),
        re.compile(r"^\s*role\s*:\s*(.+)$", re.I),
    ]
    for line in lines[:12]:
        for pattern in title_patterns:
            match = pattern.match(line)
            if match:
                return match.group(1).strip()

    fallback = re.search(
        r"\b(senior|junior|lead|principal|staff)?\s*(software|backend|frontend|full\s*stack|data|devops|ml)?\s*(engineer|developer|analyst|scientist)\b",
        text,
        re.I,
    )
    if fallback:
        return re.sub(r"\s+", " ", fallback.group(0)).strip().title()
    return "Unknown"


def _extract_seniority(text: str) -> str:
    lower = text.lower()
    senior_hits = sum(
        lower.count(k)
        for k in ["senior", "lead", "principal", "staff", "8+ years", "7+ years", "6+ years"]
    )
    mid_hits = sum(lower.count(k) for k in ["mid", "intermediate", "3+ years", "4+ years", "5+ years"])
    entry_hits = sum(lower.count(k) for k in ["entry", "junior", "fresher", "0-2 years", "1+ years", "graduate"])

    if senior_hits >= max(mid_hits, entry_hits):
        return "senior"
    if mid_hits >= max(senior_hits, entry_hits):
        return "mid"
    return "entry"


def _extract_domain(text: str) -> str:
    lower = text.lower()
    scores = {domain: sum(lower.count(term) for term in terms) for domain, terms in DOMAIN_KEYWORDS.items()}
    domain = max(scores, key=scores.get)
    return domain if scores[domain] > 0 else "general"


def _extract_required_experience_years(text: str) -> float | None:
    patterns = [
        r"(\d+)\+?\s*(?:years|yrs)\s+(?:of\s+)?experience",
        r"minimum\s+(\d+)\s*(?:years|yrs)",
        r"at\s+least\s+(\d+)\s*(?:years|yrs)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return float(match.group(1))
    return None


def _extract_skills(text: str) -> tuple[list[str], list[str]]:
    lower = text.lower()
    required: set[str] = set()
    preferred: set[str] = set()

    preferred_triggers = ["preferred", "nice to have", "bonus", "plus", "good to have"]

    for skill in SKILL_KEYWORDS:
        if skill in lower:
            is_preferred = False
            for trigger in preferred_triggers:
                pattern = rf"{trigger}[\s\S]{{0,120}}{re.escape(skill)}"
                if re.search(pattern, lower):
                    is_preferred = True
                    break
            if is_preferred:
                preferred.add(skill)
            else:
                required.add(skill)

    required_clean = sorted({s.title() if s != "ci/cd" else "CI/CD" for s in required - preferred})
    preferred_clean = sorted({s.title() if s != "ci/cd" else "CI/CD" for s in preferred})
    return required_clean, preferred_clean


def _extract_responsibilities(text: str) -> list[str]:
    lines = [line.strip("•-* ").strip() for line in text.splitlines() if line.strip()]
    responsibilities: list[str] = []
    keywords = ["responsibilit", "you will", "what you'll do", "key duties", "role includes"]

    for idx, line in enumerate(lines):
        low = line.lower()
        if any(key in low for key in keywords):
            for follow in lines[idx + 1 : idx + 8]:
                if len(follow.split()) >= 4:
                    responsibilities.append(follow)
            break

    if not responsibilities:
        bullet_like = [line for line in lines if len(line.split()) >= 6 and re.search(r"\b(build|develop|design|manage|lead|implement)\b", line, re.I)]
        responsibilities = bullet_like[:6]
    return responsibilities[:8]


def _extract_certifications(text: str) -> list[str]:
    lower = text.lower()
    found = [cert for cert in CERTIFICATION_PATTERNS if cert in lower]
    normalized = []
    for cert in found:
        if cert == "pmp":
            normalized.append("PMP")
        elif cert in {"cka", "ckad"}:
            normalized.append(cert.upper())
        else:
            normalized.append(cert.title())
    return sorted(set(normalized))


def parse_job_description(jd_text: str) -> dict[str, Any]:
    text = (jd_text or "").strip()
    if not text:
        raise ValueError("Job description cannot be empty.")

    required_skills, preferred_skills = _extract_skills(text)

    return {
        "job_title_detected": _extract_job_title(text),
        "domain": _extract_domain(text),
        "seniority_level": _extract_seniority(text),
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "required_experience_years": _extract_required_experience_years(text),
        "key_responsibilities": _extract_responsibilities(text),
        "certifications_required": _extract_certifications(text),
    }
