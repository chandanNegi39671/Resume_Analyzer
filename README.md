# Resume Analyzer

Resume Analyzer is a local-first FastAPI + React application that evaluates a resume against a job description for an ML Intern role.  
The backend is the only layer that talks to Ollama and always returns structured JSON for the frontend dashboard.

## Architecture

- Frontend: React (`frontend/`)
- Backend: FastAPI (`backend/`)
- LLM runtime: Local Ollama only
- Main API endpoints:
  - `GET /api/health`
  - `POST /api/analyze`

## Ollama-Only Configuration

Set backend environment variables in `backend/.env`:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=gemma:2b
OLLAMA_TIMEOUT=60
FRONTEND_ORIGIN=http://localhost:5173
MAX_FILE_SIZE_MB=5
```

Only `OLLAMA_*` variables control model backend behavior.

## Local Setup

### 1) Start Ollama

```bash
ollama serve
ollama pull gemma:2b
```

### 2) Start backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3) Start frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`  
Backend URL: `http://localhost:8000`

## API Behavior

### `GET /api/health`

Performs a real Ollama check by calling Ollama `/api/tags` and validates that `OLLAMA_MODEL` is installed.

Healthy response includes:
- `status`
- `base_url`
- `model`
- `available_models`

Unhealthy responses return actionable diagnostics with `code` and `details`.

### `POST /api/analyze`

Accepts multipart form:
- `resume_file` (`.pdf` or `.docx`, max 5MB)
- `jd_text` (50-5000 chars)

Flow:
- Parse resume and JD
- Build short deterministic prompt for ML Intern analysis
- Call Ollama with low-temperature JSON output
- Validate and normalize response to stable schema
- Return JSON to frontend

Error handling:
- `400`: input/parsing errors
- `502`: invalid or malformed upstream AI output
- `503`: Ollama unreachable, timeout, or model missing

## Notes

- No hosted model APIs are used.
- Frontend has no model selection logic.
- Keep `OLLAMA_MODEL` centralized in backend env configuration.
