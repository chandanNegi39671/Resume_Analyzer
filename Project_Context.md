# Project_Context.md — Resume Analyzer
> **Single Source of Truth** for all development sessions, AI coding assistants, and architectural decisions.
> Last updated: 2025. Do not delete or restructure this file without updating all dependent session prompts.

---

## 1. Project Overview

**Product Name:** Resume Analyzer
**Type:** AI-powered SaaS-grade web application (final-year project)
**Domain:** Career tech / HR tech / Recruitment automation

Resume Analyzer is an AI-powered application that parses resumes and compares them against job descriptions. It evaluates ATS compatibility, measures job fit, scores project relevance, estimates shortlist probability, and provides structured, actionable improvement suggestions. The output is rendered as a professional dashboard with scoring panels and rewrite suggestions.

This project is built to production-grade standards — not a demo. Every decision should reflect how a real HR-tech product would be built.

**Primary Tech Stack:**
- **Frontend:** React + Tailwind CSS
- **Backend:** FastAPI (Python)
- **AI Layer:** Local Ollama API (`OLLAMA_MODEL` from backend environment)
- **File Parsing:** PyMuPDF / pdfplumber for PDF, python-docx for DOCX
- **Deployment Target:** Vercel (frontend) + Railway / Render (backend)

---

## 2. Vision

Build a resume intelligence tool that gives candidates and recruiters a clear, structured signal on resume quality, job alignment, and screening probability — delivered through an explainable, dashboard-style interface that feels like a real product.

The system should be useful on day one and extensible toward a genuine SaaS product: multi-user accounts, recruiter dashboards, batch processing, and API access.

---

## 3. Problem Statement

**Candidates** submit resumes without knowing:
- Whether their resume passes ATS filters before a human sees it
- How closely their skills and experience match the target job description
- Which keywords or skills are missing
- Why their projects may not appear relevant to recruiters
- What specific changes would improve their shortlisting chances

**Recruiters and placement cells** lack:
- A fast, structured way to evaluate resume–JD alignment at scale
- Consistent scoring across candidates
- Automated pre-screening signals before manual review

Existing tools either give vague feedback, have poor UX, or are locked behind expensive subscriptions. This product fills that gap with transparent, AI-generated scoring and recommendations.

---

## 4. Core Product Goals

1. Determine whether a resume is ATS-friendly (structure, formatting, keyword density)
2. Compare the resume against a provided job description and score the alignment
3. Score skills, keywords, education, experience, and project relevance independently
4. Estimate shortlist probability as a screening-stage fit score
5. Provide actionable, specific improvement recommendations per section
6. Suggest rewrites for weak bullet points or project descriptions
7. Return a stable, structured JSON response that the frontend renders deterministically
8. Support future expansion to multi-user, recruiter, and batch-processing modes

---

## 5. Non-Goals

- This product does **not** apply to jobs on behalf of users
- It does **not** guarantee shortlisting or hiring outcomes
- It does **not** store or train on user resume data beyond the active session (unless auth + storage is explicitly added in a future sprint)
- It does **not** scrape job postings — users paste or upload JDs
- It does **not** generate full resume PDFs (improvement suggestions only, no layout generation in v1)
- It does **not** handle video resumes, LinkedIn scraping, or portfolio analysis in v1

---

## 6. Target Users

| User Type | Primary Need |
|---|---|
| **Students / Freshers** | Understand how strong their resume is before applying |
| **Career switchers** | Check if existing experience maps to a new domain |
| **Experienced professionals** | Fine-tune resume for a specific role |
| **Placement cells** | Pre-screen student resumes at scale |
| **Recruiters** | Quickly gauge candidate–JD fit without reading full resumes |

---

## 7. Core Features

### 7.1 Resume Upload & Parsing
- Accept PDF and DOCX formats
- Extract text, structure sections (Education, Experience, Skills, Projects, Summary)
- Detect formatting signals: columns, tables, graphics, fonts, non-standard characters

### 7.2 Job Description Input
- Free-text paste or structured form input
- Extract required skills, preferred skills, job title, seniority level, domain

### 7.3 ATS Friendliness Analysis
- Check for ATS-incompatible formatting (tables, columns, images, headers/footers)
- Measure keyword density and placement
- Check for standard section headings
- Detect use of special characters, non-parsable fonts, or graphics
- Return ATS score (0–100) with per-issue breakdown

### 7.4 Job Match Analysis
- Skills overlap: required vs. present
- Domain alignment: does the resume's experience domain match JD domain?
- Seniority alignment: does experience level match the role?
- Education match: degree, field, certification relevance
- Keyword coverage: important JD terms present/absent in resume

### 7.5 Project Relevance Scoring
- Analyze each listed project against the JD
- Rate relevance per project (High / Medium / Low / Irrelevant)
- Explain why a project is or isn't relevant to the target role
- Suggest how to reframe or reword project descriptions for better alignment

### 7.6 Shortlist Probability Estimation
- Combine ATS score, job match score, experience alignment, and keyword coverage
- Output a probability range (e.g., 60–70%) with a confidence band
- Clearly label as **estimate** — based on pattern matching, not recruiter access
- Include a plain-language explanation of what is driving the estimate up or down

### 7.7 Improvement Plan
- Per-section recommendations (Skills, Summary, Experience, Projects)
- Missing keyword suggestions with context
- Rewrite suggestions for weak bullet points
- Priority-ordered action list (High / Medium / Low impact)

### 7.8 Final Verdict
- Overall assessment in plain language
- Strengths of the resume relative to the JD
- Critical gaps that must be addressed
- Recommended next steps

---

## 8. Key Differentiators

| Feature | What Sets This Apart |
|---|---|
| **ATS Friendliness Analysis** | Breaks down specific formatting and keyword issues, not just a vague pass/fail |
| **Project Relevance Scoring** | Each project is individually scored and explained against the JD |
| **Shortlist Probability** | Transparent, ranged estimate with reasoning — not a black-box number |
| **Explainable Recommendations** | Every suggestion explains *why* it matters, not just what to change |
| **Dashboard UI** | Professional scoring panels, not a plain text output |
| **Stable JSON Contract** | Frontend renders deterministically from structured AI output |

---

## 9. Functional Requirements

### FR-001: File Handling
- Accept PDF (all versions) and DOCX
- Maximum file size: 5MB
- Extract text preserving section order
- Fallback: if PDF is image-based, return error with clear message (OCR is future scope)

### FR-002: JD Input
- Accept minimum 50 characters, maximum 5000 characters of job description text
- Extract job title, required skills, preferred skills, experience level, and domain

### FR-003: Analysis Pipeline
- Parse resume → extract structured fields
- Parse JD → extract structured fields
- Run AI analysis across all scoring dimensions
- Return structured JSON within 30 seconds for typical resume + JD pair

### FR-004: Scoring
- All scores on 0–100 scale unless stated otherwise
- Shortlist probability returned as a percentage range (e.g., "55–65%")
- Scores must be explainable — each score must have a reason array

### FR-005: Response Stability
- The JSON schema defined in Section 17 must not change between requests for the same input
- Frontend must be able to render without conditional null checks on required fields
- All required fields must always be present (use empty arrays/strings, never omit keys)

### FR-006: Error States
- Parsing failure → return structured error JSON, not a 500
- AI timeout → retry once, then return partial result with `incomplete: true` flag
- Unsupported file type → return validation error before hitting AI layer

---

## 10. Non-Functional Requirements

| Requirement | Target |
|---|---|
| **Response Time** | < 30s for full analysis (AI-bound) |
| **Availability** | 99% uptime for demo; SLA not required in v1 |
| **Scalability** | Handle 10 concurrent requests without queue; async queue for > 10 |
| **Security** | No persistent storage of resume content in v1 unless user auth is added |
| **Accessibility** | WCAG 2.1 AA for core UI elements |
| **Browser Support** | Chrome, Firefox, Edge, Safari (last 2 major versions) |
| **Mobile** | Responsive layout; upload + view results on mobile |
| **Error Transparency** | All errors surfaced to user in plain language |

---

## 11. End-to-End User Flow

```
[User lands on homepage]
        │
        ▼
[Upload Resume (PDF/DOCX)] + [Paste Job Description]
        │
        ▼
[Frontend sends multipart form to POST /api/analyze]
        │
        ▼
[Backend: Parse resume file → extract raw text + sections]
        │
        ▼
[Backend: Parse JD text → extract structured JD fields]
        │
        ▼
[Backend: Build AI prompt → call Ollama API]
        │
        ▼
[Ollama returns structured JSON analysis]
        │
        ▼
[Backend: Validate + normalize JSON → return to frontend]
        │
        ▼
[Frontend: Render dashboard with scores, panels, recommendations]
        │
        ▼
[User reviews scores → reads recommendations → downloads report (v2)]
```

---

## 12. Recommended Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                    │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │ Upload UI  │  │ JD Input UI  │  │ Results Dashboard│ │
│  └────────────┘  └──────────────┘  └─────────────────┘ │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP (multipart/form-data)
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                       │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │ File Parser  │   │  JD Parser   │   │ Prompt Builder│ │
│  │(PDF/DOCX)    │   │ (NLP extract)│   │             │ │
│  └──────────────┘   └──────────────┘   └──────┬──────┘ │
│                                               │        │
│  ┌────────────────────────────────────────────▼──────┐ │
│  │              Ollama API Client                    │ │
│  │  (local HTTP call, timeout, retry, JSON mode)     │ │
│  └────────────────────────────────────────────┬──────┘ │
│                                               │        │
│  ┌────────────────────────────────────────────▼──────┐ │
│  │           Response Validator & Normalizer         │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │ JSON
                            ▼
                     Frontend renders
```

### API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/analyze` | Main analysis endpoint |
| `GET` | `/api/health` | Health check |
| `POST` | `/api/parse-resume` | Resume parsing only (dev/debug) |
| `POST` | `/api/parse-jd` | JD parsing only (dev/debug) |

---

## 13. AI Pipeline Design

### Step 1: Resume Parsing (pre-AI)
Use PyMuPDF / pdfplumber for PDF, python-docx for DOCX. Extract:
- Raw full text
- Section-by-section breakdown (heuristic or regex-based section detection)
- ATS red flags at parse time (tables detected, images detected, multi-column layout)

### Step 2: JD Parsing (pre-AI)
Use rule-based extraction in backend parser to extract:
- Job title
- Required skills list
- Preferred skills list
- Experience level (entry / mid / senior)
- Domain / industry
- Certifications required

### Step 3: Prompt Construction
Compose a structured prompt that includes:
- Resume text (full or truncated to 3000 tokens)
- JD structured fields
- System instructions for analysis depth and output format
- JSON schema the model must fill

### Step 4: Ollama API Call
- Model: from `OLLAMA_MODEL` (example: `gemma:2b`)
- Max output tokens: constrained by local Ollama options
- Temperature: 0 (deterministic scoring)
- System prompt: enforces JSON-only output with schema

### Step 5: Response Parsing
- Parse Ollama output as JSON
- Validate all required keys are present
- Normalize score ranges
- Return to frontend

### Step 6: Error Recovery
- If JSON is malformed: retry with stricter JSON-only instruction
- If timeout (>45s): return partial result with `incomplete: true`
- If file unreadable: return structured error before AI call

---

## 14. Model Strategy

**Primary model:** backend `OLLAMA_MODEL` value
Use one local Ollama model consistently for the full analysis pipeline to keep output stable and deterministic.

**Prompt approach:**
- Use a single large prompt with all context (resume + JD + schema instructions)
- Do not use multi-turn conversation for the main analysis — stateless single-shot call
- Include few-shot examples of the expected JSON structure in the system prompt for the first 3 fields to anchor format

**Token budget:**
- System prompt: ~800 tokens
- Resume text: up to 2500 tokens (truncate from bottom if longer)
- JD text: up to 500 tokens
- Response: up to 4000 tokens
- Total budget: ~8000 tokens per request

**Fallback:** If Ollama or the configured model is unavailable, surface a clear error — do not silently switch models.

---

## 15. Backend Responsibilities

- Accept multipart form uploads (resume file + JD text)
- Parse resume files into clean structured text
- Extract JD into structured fields
- Build the AI prompt from parsed inputs
- Call Ollama API with correct parameters
- Validate and normalize the JSON response
- Return the final JSON to the frontend
- Handle all errors with structured error responses
- Log request/response metadata (no PII in logs unless explicitly enabled)
- Enforce file size and type validation before processing
- Expose CORS for the frontend domain

**Backend must never:**
- Return raw Ollama output without validation
- Expose API keys in responses or logs
- Store resume text beyond the request lifecycle (v1 constraint)

---

## 16. Frontend Responsibilities

- Provide resume upload UI (drag-drop + click) with file type/size validation
- Provide JD input textarea with character count and validation
- Show loading state with progress indication during analysis
- Render the results dashboard from the JSON response
- Display all score panels: ATS, Job Match, Project Relevance, Shortlist Probability
- Display the improvement plan as a prioritized list
- Display the final verdict section
- Handle and display error states gracefully
- Be responsive (mobile-first layout)
- Never call Ollama API directly from frontend — all AI calls go through the backend

**Dashboard panels to build:**
1. Score Overview (ATS / Match / Shortlist as visual gauges or progress bars)
2. ATS Analysis Panel (score + issue list)
3. Skills Match Panel (matched vs. missing skills as tags)
4. Project Relevance Panel (per-project relevance cards)
5. Improvement Plan Panel (tabbed: Skills / Summary / Experience / Projects)
6. Final Verdict Panel (strengths, gaps, next steps)

---

## 17. JSON Contract Expectations

> This schema is the binding contract between backend and frontend. It must not change structure between requests. All keys in `required` blocks must always be present.

```json
{
  "meta": {
    "analysis_id": "string (uuid)",
    "timestamp": "ISO8601 string",
    "model_used": "string",
    "incomplete": false
  },

  "candidate_profile": {
    "name": "string or null",
    "email": "string or null",
    "phone": "string or null",
    "detected_domain": "string",
    "detected_seniority_level": "entry | mid | senior | unclear",
    "total_experience_years": "number or null",
    "education": [
      {
        "degree": "string",
        "field": "string",
        "institution": "string",
        "year": "string or null"
      }
    ],
    "skills_detected": ["string"],
    "certifications": ["string"]
  },

  "ats_analysis": {
    "ats_score": 0,
    "ats_grade": "Poor | Fair | Good | Excellent",
    "is_ats_friendly": false,
    "issues": [
      {
        "issue_type": "string",
        "severity": "critical | moderate | minor",
        "description": "string",
        "recommendation": "string"
      }
    ],
    "keyword_density_score": 0,
    "formatting_score": 0,
    "section_structure_score": 0
  },

  "job_analysis": {
    "job_title_detected": "string",
    "domain": "string",
    "seniority_level": "entry | mid | senior",
    "required_skills": ["string"],
    "preferred_skills": ["string"],
    "required_experience_years": "number or null",
    "key_responsibilities": ["string"],
    "certifications_required": ["string"]
  },

  "match_analysis": {
    "overall_match_score": 0,
    "skills_match": {
      "score": 0,
      "matched_skills": ["string"],
      "missing_required_skills": ["string"],
      "missing_preferred_skills": ["string"],
      "extra_skills_not_in_jd": ["string"]
    },
    "experience_alignment": {
      "score": 0,
      "explanation": "string"
    },
    "education_alignment": {
      "score": 0,
      "explanation": "string"
    },
    "domain_alignment": {
      "score": 0,
      "is_same_domain": true,
      "explanation": "string"
    },
    "keyword_coverage": {
      "score": 0,
      "important_keywords_present": ["string"],
      "important_keywords_missing": ["string"]
    }
  },

  "project_analysis": {
    "projects_found": 0,
    "projects": [
      {
        "project_name": "string",
        "description_summary": "string",
        "relevance_to_jd": "high | medium | low | irrelevant",
        "relevance_score": 0,
        "why_relevant": "string",
        "rewrite_suggestion": "string or null"
      }
    ],
    "overall_project_relevance_score": 0
  },

  "shortlist_estimation": {
    "probability_range_low": 0,
    "probability_range_high": 0,
    "probability_label": "string (e.g. '55–65%')",
    "confidence": "low | medium | high",
    "disclaimer": "This is a statistical estimate based on resume–JD pattern matching. It does not represent recruiter judgment or guarantee any hiring outcome.",
    "positive_signals": ["string"],
    "negative_signals": ["string"],
    "explanation": "string"
  },

  "improvement_plan": {
    "priority_actions": [
      {
        "priority": "high | medium | low",
        "section": "Skills | Summary | Experience | Projects | Formatting | Keywords",
        "action": "string",
        "reason": "string",
        "example_rewrite": "string or null"
      }
    ],
    "keywords_to_add": ["string"],
    "skills_to_highlight": ["string"],
    "sections_to_improve": ["string"]
  },

  "final_verdict": {
    "overall_score": 0,
    "overall_grade": "Poor | Fair | Good | Strong | Excellent",
    "summary": "string (2–4 sentences)",
    "top_strengths": ["string"],
    "critical_gaps": ["string"],
    "recommended_next_steps": ["string"]
  }
}
```

**Schema rules:**
- All array fields must be present as empty arrays `[]` if no data — never `null` or omitted
- `overall_score` is a composite (see Section 18)
- `probability_range_low` and `_high` are integers 0–100
- `disclaimer` on `shortlist_estimation` must always be present verbatim or equivalent
- `meta.incomplete` is `true` only on partial failures — frontend must display a warning banner when this is `true`

---

## 18. Scoring Philosophy

All scores are on a 0–100 integer scale. Scores are not inflated — a score of 50 should feel like 50 out of 100, not a passing grade.

**ATS Score** measures how likely an ATS system is to parse the resume correctly:
- Formatting compliance (no tables, no columns, no graphics): 40 points
- Keyword presence and placement: 35 points
- Section structure and standard headings: 25 points

**Job Match Score** measures resume–JD alignment:
- Skills match (required skills covered): 40 points
- Keyword coverage: 25 points
- Domain + seniority alignment: 20 points
- Education alignment: 15 points

**Project Relevance Score** measures how relevant listed projects are to the JD:
- Average of individual project relevance scores
- Weighted toward the top 2–3 most relevant projects
- Score of 0 if no projects listed

**Shortlist Probability** is a derived estimate:
- Input: weighted combination of ATS score, Job Match score, Project Relevance score, experience alignment
- Presented as a range (±10 points) to communicate uncertainty
- This is not a guarantee — always accompanied by disclaimer

**Overall Score** (for `final_verdict.overall_score`):
```
Overall = (ATS_score × 0.20) + (JobMatch_score × 0.45) + (ProjectRelevance_score × 0.20) + (ExperienceAlignment_score × 0.15)
```

---

## 19. Suggested Score Weighting

| Dimension | Weight in Overall Score | Rationale |
|---|---|---|
| Job Match | 45% | Most direct signal of fit |
| Project Relevance | 20% | Key differentiator for students/freshers |
| ATS Friendliness | 20% | Gate before human review |
| Experience Alignment | 15% | Strong signal but not always required |

These weights are defaults. They may be adjusted per user type in future (e.g., ATS weight increases for large-company applications).

---

## 20. UI/UX Rules

- **Color system:** Use semantic colors for scores: Red (0–39), Amber (40–59), Yellow (60–74), Green (75–89), Emerald (90–100)
- **Score display:** Circular progress rings or horizontal gauge bars — not plain text numbers alone
- **Layout:** Dashboard grid layout, not a single scrolling page of text
- **Improvement plan:** Use priority badges (red = high, amber = medium, green = low) on each action item
- **Skills tags:** Matched skills in green, missing skills in red, preferred/bonus skills in blue
- **Project cards:** Each project gets its own card with relevance badge and expandable rewrite suggestion
- **Shortlist probability:** Display as a range with a label. Always show disclaimer below it
- **Loading state:** Show skeleton loaders per panel — not a full-page spinner
- **Errors:** Display inline in the relevant section, not only as toast notifications
- **Typography:** Consistent heading hierarchy — do not use large bold text for everything
- **Whitespace:** Generous card padding — this should feel like a SaaS dashboard, not a form result
- **Mobile:** Stack panels vertically on mobile; score overview should be visible above fold

---

## 21. Demo Priorities

When demonstrating this project, prioritize showing:

1. **ATS analysis panel** — most visually impactful and immediately understandable
2. **Skills match panel** — green/red tag visualization communicates gap clearly
3. **Shortlist probability** — most memorable and conversation-starting feature
4. **Project relevance cards** — differentiator feature that most tools don't have
5. **Improvement plan** — shows practical value beyond just scoring

Prepare 2–3 demo resume + JD pairs:
- Strong match (85+ overall score)
- Weak match (35–50 overall score) — shows the gap clearly
- Career switcher case — domain mismatch but transferable skills

---

## 22. Error Handling Strategy

### Frontend Errors
| Scenario | Behavior |
|---|---|
| Wrong file type | Validate before upload, show inline error |
| File too large | Validate before upload, show size limit |
| Network failure | Show retry button, preserve input |
| API timeout | Show "Analysis is taking longer than usual" with retry |
| Partial result (`incomplete: true`) | Show warning banner, render available data |

### Backend Errors
| Scenario | Response |
|---|---|
| File parse failure | `400` with `{error: "parse_failed", message: "...", code: "PARSE_001"}` |
| JD too short | `400` with `{error: "jd_invalid", message: "...", code: "JD_001"}` |
| AI API failure | `502` with `{error: "ai_unavailable", message: "...", code: "AI_001"}` |
| JSON parse failure from AI | Retry once, then return `incomplete: true` partial |
| Unexpected server error | `500` with generic message, log full trace server-side |

All error responses follow:
```json
{
  "error": "error_code",
  "message": "Human-readable description",
  "code": "DOMAIN_XXX",
  "incomplete": true
}
```

---

## 23. Privacy and Safety Notes

- **No persistent storage** of resume content or PII in v1 unless auth/storage sprint is explicitly started
- **No logging of resume text** — log only metadata (file size, processing time, score ranges)
- **No third-party analytics** that could capture form input content
- **Configuration safety:** Ollama URL/model config stored only in backend environment variables — never in frontend code
- **File handling:** Uploaded files processed in memory and discarded after response — not written to disk in production
- **Shortlist probability disclaimer:** Always present in both API response and UI — must not be removed
- **No bias amplification:** The prompt must instruct the model to evaluate skills and experience only — not to make inferences about demographic signals from name, location, or institution alone
- **GDPR readiness note:** If deployed in EU, a data processing notice and session-based data deletion must be implemented before public launch

---

## 24. Evaluation Metrics

### Technical Metrics
- Response time P50 / P95 (target: P50 < 20s, P95 < 35s)
- JSON parse success rate (target: > 98%)
- File parse success rate for valid PDFs and DOCX (target: > 95%)
- Error rate (target: < 2% of valid requests)

### Quality Metrics (manual evaluation)
- Score calibration: Run 10 resume + JD pairs with known quality levels. Verify scores rank correctly (stronger resume should score higher).
- Recommendation quality: Verify improvement suggestions are specific, actionable, and accurate for 10 test cases
- Shortlist probability sanity check: Probability range should directionally match human recruiter judgment in 80%+ of test cases

### Demo Metrics
- Time to first result from upload < 30 seconds
- UI renders without blank panels on all test cases
- Error states display correctly for invalid inputs

---

## 25. Future Roadmap

### Phase 2 (Post-Demo / MVP+)
- User authentication (Clerk or Supabase Auth)
- Save and compare multiple resume versions
- Resume history dashboard per user
- PDF report download of analysis results

### Phase 3 (SaaS v1)
- Recruiter account type with batch upload (up to 50 resumes vs. one JD)
- Candidate ranking by match score
- Custom scoring weight profiles per recruiter
- API access with rate limiting and API key management

### Phase 4 (Growth)
- Placement cell portal with cohort analytics
- Resume builder integrated with analysis feedback
- LinkedIn profile URL input (scrape + parse)
- Role-specific prompt tuning (SWE, Data Science, Marketing, Finance)
- Multilingual resume support
- ATS-optimized resume rewrite generation (full section rewrites)

---

## 26. Prompt Engineering Rules for Future AI Sessions

> Any AI assistant working on this project must follow these rules.

### Core Rules
1. **Always return valid JSON** matching the schema in Section 17 exactly. Do not add, remove, or rename keys.
2. **Temperature must be 0** for the analysis call. No creative variation in scoring.
3. **Scores must be integers 0–100.** Do not return decimals, strings, or out-of-range values.
4. **All required array fields must be present** even if empty. Never omit a key.
5. **The shortlist disclaimer must always be present** in `shortlist_estimation.disclaimer`.
6. **Do not infer demographics** from candidate name, institution name, or location when scoring.

### System Prompt Template (reference)
```
You are a professional resume analysis engine. Analyze the provided resume against the job description.
Return ONLY a valid JSON object. Do not include any text before or after the JSON.
Follow this exact schema: [SCHEMA HERE]
Score all dimensions on 0–100 integer scale.
Be accurate and calibrated — do not inflate scores.
Shortlist probability is an estimate only. Always include the disclaimer.
```

### Prompt Construction Order
1. System prompt (schema + rules)
2. Resume text block (labeled `RESUME:`)
3. JD structured fields block (labeled `JOB_DESCRIPTION:`)
4. Output instruction: `Return only the JSON object. No markdown. No explanation.`

### What to Avoid in Prompts
- Do not ask the model to "be encouraging" or "be positive" — this inflates scores
- Do not include examples of high scores — anchoring effect will bias output
- Do not use vague instructions like "analyze well" — be explicit about each dimension

---

## 27. Dev Workflow Rules

> Rules for all developers and AI assistants contributing to this project.

1. **Schema changes require version bump.** If `JSON contract` in Section 17 changes, update `meta.schema_version` and notify frontend.
2. **No direct Ollama API calls from frontend.** All AI calls go through the FastAPI backend.
3. **Environment variables only for secrets.** API key, model name, and environment flags go in `.env` — never hardcoded.
4. **Validate before calling AI.** File parsing, JD validation, and size checks happen before the AI call is made.
5. **Normalize AI output before returning.** Never return raw Ollama JSON to frontend without schema validation.
6. **Feature flags for future features.** Wrap unreleased features in `FEATURE_X_ENABLED` env flags.
7. **No mock data in production paths.** Test fixtures live in `/tests` only.
8. **Frontend renders from JSON only.** Frontend components must not contain hardcoded analysis logic — all scoring, labels, and recommendations come from the API.
9. **All new backend routes must have a corresponding error response documented.**
10. **Use `incomplete: true` correctly.** Only set when data is genuinely partial — not as a default.

### File Structure (reference)
```
resume-analyzer/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── upload/
│   │   │   ├── dashboard/
│   │   │   │   ├── ATSPanel.jsx
│   │   │   │   ├── MatchPanel.jsx
│   │   │   │   ├── ProjectsPanel.jsx
│   │   │   │   ├── ShortlistPanel.jsx
│   │   │   │   ├── ImprovementPanel.jsx
│   │   │   │   └── VerdictPanel.jsx
│   │   │   └── shared/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── App.jsx
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── analyze.py
│   │   ├── parsers/
│   │   │   ├── resume_parser.py
│   │   │   └── jd_parser.py
│   │   ├── ai/
│   │   │   ├── ollama_client.py
│   │   │   ├── prompt_builder.py
│   │   │   └── response_validator.py
│   │   └── models/
│   │       └── schemas.py
│   ├── tests/
│   └── .env.example
├── Project_Context.md   ← this file
└── README.md
```

---

## 28. Final Positioning Statement

Resume Analyzer is a production-grade AI application that solves a real problem for students, freshers, and career switchers — making resume screening transparent, structured, and actionable.

It is built with a stable JSON contract, explainable scoring, and a premium dashboard UI. The shortlist probability feature is its defining differentiator — honest, ranged, and always disclaimed.

This is not a demo. Every architectural decision should be made as if this will be used by real users. The AI pipeline is deterministic, the schema is binding, and the UI reflects a SaaS product — not a college submission.

**If you are an AI assistant reading this file:** treat this document as the authoritative source of truth for all decisions. Do not deviate from the JSON schema in Section 17. Do not change scoring weights without updating Section 19. Do not add features not listed here without noting them as out of scope. When in doubt, ask before changing anything structural.

---

*End of Project_Context.md*
