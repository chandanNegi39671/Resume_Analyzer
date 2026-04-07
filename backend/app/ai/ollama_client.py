from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

import requests


DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_MODEL = "gemma:2b"
DEFAULT_OLLAMA_TIMEOUT = 60


@dataclass
class OllamaClientError(Exception):
    message: str
    code: str = "AI_001"
    status_code: int = 503
    details: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL).strip().rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL).strip() or DEFAULT_OLLAMA_MODEL
        self.timeout = float(os.getenv("OLLAMA_TIMEOUT", str(DEFAULT_OLLAMA_TIMEOUT)))

    @staticmethod
    def _strip_code_fences(value: str) -> str:
        cleaned = value.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        return cleaned

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method=method, url=url, json=payload, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise OllamaClientError(
                message=f"Ollama timed out after {int(self.timeout)}s.",
                code="AI_002",
                status_code=503,
                details={"base_url": self.base_url, "model": self.model},
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise OllamaClientError(
                message="Could not reach Ollama. Ensure `ollama serve` is running.",
                code="AI_001",
                status_code=503,
                details={"base_url": self.base_url, "model": self.model},
            ) from exc

        if response.status_code >= 400:
            error_message = response.text
            try:
                error_payload = response.json()
                if isinstance(error_payload, dict):
                    error_message = str(error_payload.get("error") or error_payload.get("message") or error_payload)
            except Exception:
                pass
            error_code = "AI_003" if response.status_code in {400, 404} else "AI_004"
            raise OllamaClientError(
                message=f"Ollama request failed ({response.status_code}): {error_message}",
                code=error_code,
                status_code=503 if response.status_code in {400, 404} else 502,
                details={"base_url": self.base_url, "model": self.model, "http_status": response.status_code},
            )

        try:
            payload = response.json()
        except Exception as exc:
            raise OllamaClientError(
                message="Ollama returned non-JSON HTTP payload.",
                code="AI_004",
                status_code=502,
                details={"base_url": self.base_url, "model": self.model},
            ) from exc

        if not isinstance(payload, dict):
            raise OllamaClientError(
                message="Ollama response payload is not a JSON object.",
                code="AI_004",
                status_code=502,
                details={"base_url": self.base_url, "model": self.model},
            )

        return payload

    def check_health(self) -> dict[str, Any]:
        payload = self._request(method="GET", path="/api/tags")
        models = payload.get("models", [])
        available_models = []
        if isinstance(models, list):
            available_models = [m.get("name") for m in models if isinstance(m, dict) and m.get("name")]
        model_available = self.model in available_models
        if not model_available:
            raise OllamaClientError(
                message=f"Configured model '{self.model}' is not installed in Ollama.",
                code="AI_003",
                status_code=503,
                details={
                    "configured_model": self.model,
                    "available_models": available_models,
                    "base_url": self.base_url,
                },
            )
        return {
            "base_url": self.base_url,
            "configured_model": self.model,
            "available_models": available_models,
            "model_available": True,
        }

    def _single_call(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0, "num_predict": 900},
        }
        response_payload = self._request(method="POST", path="/api/generate", payload=payload)
        response_text = str(response_payload.get("response", "")).strip()
        if not response_text:
            raise OllamaClientError(
                message="Ollama returned an empty generation response.",
                code="AI_004",
                status_code=502,
                details={"base_url": self.base_url, "model": self.model},
            )
        return response_text

    def _single_call_with_retry(self, system_prompt: str, user_prompt: str) -> str:
        last_error: OllamaClientError | None = None
        for attempt in range(2):
            try:
                return self._single_call(system_prompt=system_prompt, user_prompt=user_prompt)
            except OllamaClientError as exc:
                last_error = exc
                http_status = int(exc.details.get("http_status", 0)) if isinstance(exc.details, dict) else 0
                should_retry = exc.code == "AI_004" and http_status >= 500 and attempt == 0
                if not should_retry:
                    raise
                time.sleep(1)
        if last_error:
            raise last_error
        raise OllamaClientError(message="Ollama call failed.", code="AI_004", status_code=502)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.check_health()
        first_response = self._single_call_with_retry(system_prompt=system_prompt, user_prompt=user_prompt)
        cleaned_first = self._strip_code_fences(first_response)
        try:
            json.loads(cleaned_first)
            return cleaned_first
        except json.JSONDecodeError:
            retry_prompt = (
                f"{user_prompt}\n\n"
                "Return exactly one valid JSON object only."
            )
            second_response = self._single_call_with_retry(system_prompt=system_prompt, user_prompt=retry_prompt)
            cleaned_second = self._strip_code_fences(second_response)
            try:
                json.loads(cleaned_second)
                return cleaned_second
            except json.JSONDecodeError as exc:
                raise OllamaClientError(
                    message="Ollama returned invalid JSON in two attempts.",
                    code="AI_005",
                    status_code=502,
                    details={"base_url": self.base_url, "model": self.model},
                ) from exc
