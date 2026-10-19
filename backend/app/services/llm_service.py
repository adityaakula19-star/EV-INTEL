from __future__ import annotations

import httpx

from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.services.data_service import build_evidence


class LLMConfigurationError(RuntimeError):
    pass


def _require_api_key() -> str:
    if not settings.llm_api_key:
        raise LLMConfigurationError(
            "LLM_API_KEY is missing. Add it to backend/.env and restart the backend. "
            "The key is never sent to the frontend."
        )
    return settings.llm_api_key


def _user_message(question: str, question_type: str, evidence: list[str]) -> str:
    evidence_block = "\n".join(f"- {item}" for item in evidence) if evidence else "- No dataset evidence was retrieved."
    return (
        f"Question type classified by backend: {question_type}\n\n"
        f"User question:\n{question}\n\n"
        f"Dataset evidence from the backend (source of truth for numbers):\n{evidence_block}\n\n"
        "Literature retrieval is not enabled in this build.\n"
        "Use only the evidence above for numerical claims. If a number is not present, say it is unavailable."
    )


def call_llm(question: str, question_type: str, evidence: list[str]) -> str:
    api_key = _require_api_key()
    url = f"{settings.llm_base_url}/chat/completions"
    payload = {
        "model": settings.llm_model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _user_message(question, question_type, evidence)},
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
        response = client.post(url, headers=headers, json=payload)
    if response.status_code >= 400:
        raise RuntimeError(
            f"LLM API request failed with status {response.status_code}: {response.text[:500]}"
        )
    data = response.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("LLM API returned an unexpected response shape.") from exc
    if not content or not str(content).strip():
        raise RuntimeError("LLM API returned an empty answer.")
    return str(content).strip()


def answer_question(question: str) -> dict:
    cleaned = (question or "").strip()
    if not cleaned:
        return {
            "question": question,
            "question_type": "invalid",
            "countries": [],
            "years": [],
            "evidence": [],
            "answer": "Please enter a non-empty question.",
            "model": settings.llm_model,
            "llm_used": False,
            "error": "empty_question",
        }

    question_type, countries, years, evidence = build_evidence(cleaned)
    try:
        answer = call_llm(cleaned, question_type, evidence)
        return {
            "question": cleaned,
            "question_type": question_type,
            "countries": countries,
            "years": years,
            "evidence": evidence,
            "answer": answer,
            "model": settings.llm_model,
            "llm_used": True,
            "error": None,
        }
    except LLMConfigurationError as exc:
        return {
            "question": cleaned,
            "question_type": question_type,
            "countries": countries,
            "years": years,
            "evidence": evidence,
            "answer": (
                "The LLM is not configured. Numerical evidence from the dataset is still shown. "
                + str(exc)
            ),
            "model": settings.llm_model,
            "llm_used": False,
            "error": "missing_api_key",
        }
    except Exception as exc:
        return {
            "question": cleaned,
            "question_type": question_type,
            "countries": countries,
            "years": years,
            "evidence": evidence,
            "answer": "The LLM request failed. Dataset evidence is still available below.",
            "model": settings.llm_model,
            "llm_used": False,
            "error": str(exc),
        }
