import PyPDF2
import re
from .job_data import JOB_DATABASE

SKILL_ALIASES = {
    "javascript": ["js", "javascript"],
    "react": ["react", "reactjs"],
    "node": ["node", "nodejs"],
    "python": ["python", "py"],
}

# PDF -> Text
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


# Extract Email
def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None

# Extract Phone Number
def extract_phone(text):
    pattern = r"\+?\d[\d\s-]{8,}\d"
    match = re.search(pattern, text)
    return match.group(0) if match else None



# Extract Resume Skills Based On JOB_DATABASE
def extract_resume_skills(resume_text):
    resume_text = resume_text.lower()
    found_skills = set()

    for job in JOB_DATABASE.values():
        for skill in job["skills"]:
            skill_lower = skill.lower()

            # Get aliases for this skill
            aliases = SKILL_ALIASES.get(skill_lower, [skill_lower])

            for alias in aliases:
                if alias in resume_text:
                    found_skills.add(skill_lower)
                    break

    return list(found_skills)



# Analyze Job Match
def analyze_job_match(resume_skills, job_title):

    job_title = job_title.lower()

    if job_title not in JOB_DATABASE:
        return {
        "error": "Job title not available in database"
    }

    required_skills = JOB_DATABASE[job_title]["skills"]

    # Convert resume skills to lowercase
    resume_skills = [skill.lower() for skill in resume_skills]

    matched_skills = []
    missing_skills = []

    for req_skill in required_skills:
        req_skill_lower = req_skill.lower()

        # Get aliases if exist
        aliases = SKILL_ALIASES.get(req_skill_lower, [req_skill_lower])

        found = False

        for alias in aliases:
            if alias in resume_skills:
                found = True
                break

        if found:
            matched_skills.append(req_skill)
        else:
            missing_skills.append(req_skill)

    score = (len(matched_skills) / len(required_skills)) * 100
    qualified = score >= 70

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(score, 2),
        "qualified": qualified
    }





# Match Skills

# def match_skills(resume_text, job_desc):
#     resume_words = resume_text.lower().split()
#     job_words = job_desc.lower().split()

#     matched = set(resume_words) & set(job_words)

#     score = (len(matched) / len(set(job_words))) * 100 if job_words else 0

#     return list(matched), round(score, 2)