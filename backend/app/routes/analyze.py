import logging
import os
from typing import Any

from dotenv import load_dotenv
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from app.ai.ollama_client import OllamaClient, OllamaClientError
from app.ai.prompt_builder import build_prompts
from app.ai.response_validator import validate_and_normalize_response
from app.models.schemas import AnalysisResponse
from app.parsers.jd_parser import parse_job_description
from app.parsers.resume_parser import parse_resume

load_dotenv()

logger = logging.getLogger("resume-analyzer")
router = APIRouter(prefix="/api", tags=["analysis"])

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _error_payload(
    error: str,
    message: str,
    code: str,
    status_code: int,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    payload: dict[str, Any] = {
        "error": error,
        "message": message,
        "code": code,
        "incomplete": True,
    }
    if details:
        payload["details"] = details
    return JSONResponse(status_code=status_code, content=payload)


@router.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...),
) -> Any:
    filename = (resume_file.filename or "").strip().lower()
    extension = f".{filename.rsplit('.', 1)[-1]}" if "." in filename else ""
    mime_type = (resume_file.content_type or "").strip().lower()

    if extension not in ALLOWED_EXTENSIONS:
        return _error_payload(
            error="unsupported_file_type",
            message="Only PDF and DOCX files are supported.",
            code="FILE_001",
            status_code=400,
        )

    if mime_type not in ALLOWED_MIME_TYPES:
        return _error_payload(
            error="unsupported_mime_type",
            message="Uploaded file MIME type is invalid. Use a valid PDF or DOCX file.",
            code="FILE_002",
            status_code=400,
        )

    if not isinstance(jd_text, str):
        return _error_payload(
            error="jd_invalid",
            message="Job description must be text.",
            code="JD_001",
            status_code=400,
        )

    jd_text = jd_text.strip()
    if len(jd_text) < 50 or len(jd_text) > 5000:
        return _error_payload(
            error="jd_invalid",
            message="Job description must be between 50 and 5000 characters.",
            code="JD_001",
            status_code=400,
        )

    try:
        file_bytes = await resume_file.read()
    except Exception:
        return _error_payload(
            error="file_read_failed",
            message="Unable to read the uploaded file.",
            code="FILE_003",
            status_code=400,
        )

    if len(file_bytes) == 0:
        return _error_payload(
            error="empty_file",
            message="Uploaded file is empty.",
            code="FILE_004",
            status_code=400,
        )

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return _error_payload(
            error="file_too_large",
            message=f"File size exceeds {MAX_FILE_SIZE_MB}MB limit.",
            code="FILE_005",
            status_code=400,
        )

    try:
        resume_data = parse_resume(file_bytes=file_bytes, mime_type=mime_type)
    except ValueError as exc:
        return _error_payload(
            error="parse_failed",
            message=str(exc),
            code="PARSE_001",
            status_code=400,
        )
    except Exception:
        logger.exception("Resume parsing failed")
        return _error_payload(
            error="parse_failed",
            message="Resume parsing failed. Please upload a readable PDF or DOCX.",
            code="PARSE_001",
            status_code=400,
        )

    try:
        jd_data = parse_job_description(jd_text)
    except Exception:
        logger.exception("JD parsing failed")
        return _error_payload(
            error="jd_invalid",
            message="Failed to parse job description.",
            code="JD_002",
            status_code=400,
        )

    try:
        prompts = build_prompts(resume_data=resume_data, jd_data=jd_data, jd_text=jd_text)
        client = OllamaClient()
        raw_response = client.generate(
            system_prompt=prompts["system_prompt"],
            user_prompt=prompts["user_prompt"],
        )
    except OllamaClientError as exc:
        return _error_payload(
            error="ai_unavailable",
            message=exc.message,
            code=exc.code,
            status_code=exc.status_code,
            details=exc.details,
        )
    except Exception:
        logger.exception("AI call failed")
        return _error_payload(
            error="ai_unavailable",
            message="AI service is unavailable. Please try again shortly.",
            code="AI_001",
            status_code=502,
        )

    try:
        normalized = validate_and_normalize_response(raw_response_text=raw_response)
        validated = AnalysisResponse.model_validate(normalized)
        return validated.model_dump()
    except Exception:
        logger.exception("Schema validation failed after normalization")
        return _error_payload(
            error="invalid_ai_response",
            message="Ollama response could not be validated against the analysis schema.",
            code="AI_006",
            status_code=502,
        )
