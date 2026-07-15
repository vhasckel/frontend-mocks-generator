"""Nó de interpretação de models TypeScript via LLM (RF03, RF04)."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from src.agent.llm import get_chat_model
from src.agent.state import MockAgentState
from src.security.validation import (
    MSG_INTERNAL,
    MSG_NO_INTERFACE,
    ValidationError,
)

# repo root / docs/prompts/interpret.md  (nodes → agent → src → root)
_PROMPT_PATH = (
    Path(__file__).resolve().parents[3] / "docs" / "prompts" / "interpret.md"
)


@lru_cache(maxsize=1)
def _load_system_prompt() -> str:
    """Carrega o prompt de sistema a partir de ``docs/prompts/interpret.md``.

    Se o arquivo tiver um bloco introdutório separado por ``---``, usa só o
    texto após o primeiro separador (corpo enviado à LLM).
    """
    raw = _PROMPT_PATH.read_text(encoding="utf-8")
    if "\n---\n" in raw:
        return raw.split("\n---\n", 1)[1].strip()
    return raw.strip()


def _has_critical_errors(state: MockAgentState) -> bool:
    if state.get("status") == "error":
        return True
    errors = state.get("errors") or []
    return len(errors) > 0


def _content_to_text(content: Any) -> str:
    """Normaliza ``response.content`` (str ou blocos multimodais) para texto."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text") or ""))
            else:
                # LangChain ContentBlock / objetos com atributo text.
                text = getattr(block, "text", None)
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    return str(content)


def _extract_json(raw: str) -> dict[str, Any]:
    """Parse JSON from the LLM response, tolerating optional markdown fences."""
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fenced:
        text = fenced.group(1).strip()
    return json.loads(text)


def _models_from_parsed(data: dict[str, Any]) -> list[dict[str, Any]]:
    models = data.get("models")
    if not isinstance(models, list):
        return []
    return [m for m in models if isinstance(m, dict) and m.get("name") and m.get("kind")]


def interpret_node(state: MockAgentState) -> dict:
    """Interpreta ``source_code`` com LLM e preenche ``parsed_model`` (RF03–RF04).

    Short-circuit se já houver erros críticos ou se ``source_code`` estiver
    ausente. Em sucesso retorna ``parsed_model``; se nenhuma estrutura
    exportada for encontrada, adiciona a mensagem da SPEC §13.
    """
    if _has_critical_errors(state):
        return {}

    source_code = (state.get("source_code") or "").strip()
    if not source_code:
        return {}

    # SPEC §12 — key só via env; falha clara sem vazar o valor.
    try:
        llm = get_chat_model()
        response = llm.invoke(
            [
                {"role": "system", "content": _load_system_prompt()},
                {
                    "role": "user",
                    "content": (
                        "Extract exported interfaces, types and enums from "
                        "this TypeScript file:\n\n"
                        f"{source_code}"
                    ),
                },
            ]
        )
        data = _extract_json(_content_to_text(response.content))
        models = _models_from_parsed(data)
    except ValidationError as exc:
        return {"errors": [exc.message], "status": "error"}
    except Exception:
        return {"errors": [MSG_INTERNAL], "status": "error"}

    if not models:
        return {"errors": [MSG_NO_INTERFACE], "status": "error"}

    # Prefer a single root model; keep siblings for generate (T5+).
    primary = models[0]
    parsed_model: dict[str, Any] = {
        "name": primary.get("name"),
        "kind": primary.get("kind"),
        "properties": primary.get("properties") or [],
        "enum_values": primary.get("enum_values") or [],
        "nested": primary.get("nested") or [],
        "models": models,
    }
    return {"parsed_model": parsed_model, "status": "running"}
