from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MetaBlock(BaseModel):
    model_config = ConfigDict(extra="ignore")
    analysis_id: str = ""
    timestamp: str = ""
    model_used: str = ""
    incomplete: bool = False


class EducationItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    degree: str = ""
    field: str = ""
    institution: str = ""
    year: str | None = None


class CandidateProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    detected_domain: str = ""
    detected_seniority_level: Literal["entry", "mid", "senior", "unclear"] = "unclear"
    total_experience_years: float | None = None
    education: list[EducationItem] = Field(default_factory=list)
    skills_detected: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ATSIssue(BaseModel):
    model_config = ConfigDict(extra="ignore")
    issue_type: str = ""
    severity: Literal["critical", "moderate", "minor"] = "minor"
    description: str = ""
    recommendation: str = ""


class ATSAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ats_score: int = Field(default=0, ge=0, le=100)
    ats_grade: Literal["Poor", "Fair", "Good", "Excellent"] = "Poor"
    is_ats_friendly: bool = False
    issues: list[ATSIssue] = Field(default_factory=list)
    keyword_density_score: int = Field(default=0, ge=0, le=100)
    formatting_score: int = Field(default=0, ge=0, le=100)
    section_structure_score: int = Field(default=0, ge=0, le=100)


class JobAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    job_title_detected: str = ""
    domain: str = ""
    seniority_level: Literal["entry", "mid", "senior"] = "entry"
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    required_experience_years: float | None = None
    key_responsibilities: list[str] = Field(default_factory=list)
    certifications_required: list[str] = Field(default_factory=list)


class SkillsMatch(BaseModel):
    model_config = ConfigDict(extra="ignore")
    score: int = Field(default=0, ge=0, le=100)
    matched_skills: list[str] = Field(default_factory=list)
    missing_required_skills: list[str] = Field(default_factory=list)
    missing_preferred_skills: list[str] = Field(default_factory=list)
    extra_skills_not_in_jd: list[str] = Field(default_factory=list)


class AlignmentBlock(BaseModel):
    model_config = ConfigDict(extra="ignore")
    score: int = Field(default=0, ge=0, le=100)
    explanation: str = ""


class DomainAlignmentBlock(BaseModel):
    model_config = ConfigDict(extra="ignore")
    score: int = Field(default=0, ge=0, le=100)
    is_same_domain: bool = False
    explanation: str = ""


class KeywordCoverage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    score: int = Field(default=0, ge=0, le=100)
    important_keywords_present: list[str] = Field(default_factory=list)
    important_keywords_missing: list[str] = Field(default_factory=list)


class MatchAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    overall_match_score: int = Field(default=0, ge=0, le=100)
    skills_match: SkillsMatch = Field(default_factory=SkillsMatch)
    experience_alignment: AlignmentBlock = Field(default_factory=AlignmentBlock)
    education_alignment: AlignmentBlock = Field(default_factory=AlignmentBlock)
    domain_alignment: DomainAlignmentBlock = Field(default_factory=DomainAlignmentBlock)
    keyword_coverage: KeywordCoverage = Field(default_factory=KeywordCoverage)


class ProjectItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    project_name: str = ""
    description_summary: str = ""
    relevance_to_jd: Literal["high", "medium", "low", "irrelevant"] = "irrelevant"
    relevance_score: int = Field(default=0, ge=0, le=100)
    why_relevant: str = ""
    rewrite_suggestion: str | None = None


class ProjectAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    projects_found: int = 0
    projects: list[ProjectItem] = Field(default_factory=list)
    overall_project_relevance_score: int = Field(default=0, ge=0, le=100)


class ShortlistEstimation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    probability_range_low: int = Field(default=0, ge=0, le=100)
    probability_range_high: int = Field(default=0, ge=0, le=100)
    probability_label: str = ""
    confidence: Literal["low", "medium", "high"] = "low"
    disclaimer: str = ""
    positive_signals: list[str] = Field(default_factory=list)
    negative_signals: list[str] = Field(default_factory=list)
    explanation: str = ""


class ImprovementAction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    priority: Literal["high", "medium", "low"] = "low"
    section: Literal["Skills", "Summary", "Experience", "Projects", "Formatting", "Keywords"] = "Skills"
    action: str = ""
    reason: str = ""
    example_rewrite: str | None = None


class ImprovementPlan(BaseModel):
    model_config = ConfigDict(extra="ignore")
    priority_actions: list[ImprovementAction] = Field(default_factory=list)
    keywords_to_add: list[str] = Field(default_factory=list)
    skills_to_highlight: list[str] = Field(default_factory=list)
    sections_to_improve: list[str] = Field(default_factory=list)


class FinalVerdict(BaseModel):
    model_config = ConfigDict(extra="ignore")
    overall_score: int = Field(default=0, ge=0, le=100)
    overall_grade: Literal["Poor", "Fair", "Good", "Strong", "Excellent"] = "Poor"
    summary: str = ""
    top_strengths: list[str] = Field(default_factory=list)
    critical_gaps: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    meta: MetaBlock = Field(default_factory=MetaBlock)
    candidate_profile: CandidateProfile = Field(default_factory=CandidateProfile)
    ats_analysis: ATSAnalysis = Field(default_factory=ATSAnalysis)
    job_analysis: JobAnalysis = Field(default_factory=JobAnalysis)
    match_analysis: MatchAnalysis = Field(default_factory=MatchAnalysis)
    project_analysis: ProjectAnalysis = Field(default_factory=ProjectAnalysis)
    shortlist_estimation: ShortlistEstimation = Field(default_factory=ShortlistEstimation)
    improvement_plan: ImprovementPlan = Field(default_factory=ImprovementPlan)
    final_verdict: FinalVerdict = Field(default_factory=FinalVerdict)
