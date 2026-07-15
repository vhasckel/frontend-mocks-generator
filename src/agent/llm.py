"""Factory do chat model (Gemini / Google AI Studio)."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.security.validation import MSG_MISSING_API_KEY, ValidationError

# Modelo padrão na faixa gratuita do Gemini Developer API (AI Studio).
_DEFAULT_MODEL = "gemini-2.0-flash"


def get_chat_model() -> ChatGoogleGenerativeAI:
    """Cria o LLM a partir de ``GOOGLE_API_KEY`` e ``GEMINI_MODEL``.

    Raises:
        ValidationError: se a API key estiver ausente (mensagem SPEC §12).
    """
    load_dotenv()
    api_key = (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key:
        raise ValidationError(MSG_MISSING_API_KEY)

    model_name = (os.getenv("GEMINI_MODEL") or _DEFAULT_MODEL).strip() or _DEFAULT_MODEL
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        google_api_key=api_key,
    )
