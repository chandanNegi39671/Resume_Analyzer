from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import (
    extract_text_from_pdf,
    extract_email,
    extract_phone,
    extract_resume_skills,
    analyze_job_match
)
# from .utils import extract_text_from_pdf, extract_email, extract_phone, match_skills


@csrf_exempt
def analyze_resume(request):
    if request.method == "POST":
        resume_file = request.FILES.get("resume")
        job_title = request.POST.get("job_title")

        if not resume_file or not job_title:
            return JsonResponse({"error": "Missing data"}, status=400)

        resume_text = extract_text_from_pdf(resume_file)

        email = extract_email(resume_text)
        phone = extract_phone(resume_text)

        resume_skills = extract_resume_skills(resume_text)

        result = analyze_job_match(resume_skills, job_title)

        if result is None:
            return JsonResponse({"error": "Job not found"}, status=404)

        return JsonResponse({
            "email": email,
            "phone": phone,
            "resume_skills": resume_skills,
            **result
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)



# @csrf_exempt

# def analyze_resume(request):
#     if request.method == "POST":
#         resume_file = request.FILES.get("resume")
#         job_desc = request.POST.get("job_desc")

#         if not resume_file or not job_desc:
#             return JsonResponse({"error": "Missing data"}, status=400)

#         # 1️⃣ Extract text
#         resume_text = extract_text_from_pdf(resume_file)

#         # 2️⃣ Extract email & phone
#         email = extract_email(resume_text)
#         phone = extract_phone(resume_text)

#         # 3️⃣ Match skills
#         matched_skills, score = match_skills(resume_text, job_desc)

#         return JsonResponse({
#             "email": email,
#             "phone": phone,
#             "matched_skills": matched_skills,
#             "match_score": score
#         })

#     return JsonResponse({"error": "Only POST allowed"}, status=405)