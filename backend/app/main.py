import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.ai.ollama_client import OllamaClient, OllamaClientError
from app.routes.analyze import router as analyze_router

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resume-analyzer")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app = FastAPI(title="Resume Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)

@app.get("/api/health")
async def health_check():
    client = OllamaClient()
    try:
        health = client.check_health()
        return {
            "status": "healthy",
            "ollama": "reachable",
            "base_url": health["base_url"],
            "model": health["configured_model"],
            "available_models": health["available_models"],
        }
    except OllamaClientError as exc:
        logger.warning("Health check failed: %s", exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "unhealthy",
                "reason": exc.message,
                "code": exc.code,
                "model": client.model,
                "base_url": client.base_url,
                "details": exc.details,
            },
        )
    except Exception as exc:
        logger.exception("Health check failed")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "reason": str(exc),
                "code": "AI_001",
                "model": client.model,
                "base_url": client.base_url,
            },
        )

@app.on_event("startup")
async def startup_event() -> None:
    client = OllamaClient()
    logger.info("Resume Analyzer backend is running with model=%s", client.model)
