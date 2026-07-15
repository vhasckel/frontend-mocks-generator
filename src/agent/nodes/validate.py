"""Nó de validação estrutural do mock gerado (RF05, RF06, RN04–RN05)."""

from __future__ import annotations

import re

from src.agent.state import MockAgentState

_MSG_EMPTY = "O mock gerado está vazio."
_MSG_INVALID = "O mock gerado é inválido ou incompatível com o modelo."
_MSG_INTERNAL = "Erro interno durante a geração do mock."


def _has_critical_errors(state: MockAgentState) -> bool:
    if state.get("status") == "error":
        return True
    errors = state.get("errors") or []
    return len(errors) > 0


def _model_property_names(parsed_model: dict) -> set[str] | None:
    """Retorna o conjunto de props do modelo root, ou None se kind for enum/sem props."""
    kind = parsed_model.get("kind")
    if kind == "enum":
        return set()
    properties = parsed_model.get("properties")
    if not isinstance(properties, list):
        return None
    names: set[str] = set()
    for prop in properties:
        if isinstance(prop, dict) and isinstance(prop.get("name"), str):
            names.add(prop["name"])
    return names


def _extract_top_level_object_props(mock_source: str) -> set[str] | None:
    """Extrai nomes de propriedades do object literal raiz do mock.

    Retorna None se não for possível localizar um object literal exportado
    (ex.: mock de enum com valor escalar).
    """
    match = re.search(
        r"export\s+const\s+\w+\s*(?::\s*[\w.]+)?\s*=\s*\{",
        mock_source,
    )
    if not match:
        return None

    start = match.end() - 1  # position of '{'
    depth = 0
    i = start
    while i < len(mock_source):
        ch = mock_source[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                body = mock_source[start + 1 : i]
                return _parse_object_keys(body)
        elif ch in ("'", '"', "`"):
            i = _skip_string(mock_source, i) + 1
            continue
        i += 1
    return None


def _skip_string(text: str, start: int) -> int:
    """Retorna o índice da aspas de fechamento (ou ``start`` se inválida)."""
    quote = text[start]
    i = start + 1
    while i < len(text):
        if text[i] == "\\" and quote != "`":
            i += 2
            continue
        if text[i] == quote:
            return i
        i += 1
    return start


def _parse_object_keys(body: str) -> set[str]:
    """Coleta chaves de primeiro nível dentro do corpo de um object literal."""
    keys: set[str] = set()
    depth = 0
    i = 0
    while i < len(body):
        ch = body[i]
        if ch in ("'", '"', "`"):
            i = _skip_string(body, i) + 1
            continue
        if ch in "{[":
            depth += 1
            i += 1
            continue
        if ch in "}]":
            depth = max(0, depth - 1)
            i += 1
            continue
        if depth == 0:
            key_match = re.match(
                r"\s*([A-Za-z_$][\w$]*)\s*:",
                body[i:],
            )
            if key_match:
                keys.add(key_match.group(1))
                i += key_match.end()
                continue
        i += 1
    return keys


def validate_node(state: MockAgentState) -> dict:
    """Valida ``generated_mock`` contra ``parsed_model``.

    Verifica conteúdo não vazio, presença das propriedades do modelo e
    ausência de propriedades extras (RN04/RN05). Em falha estrutural, seta
    ``errors`` e ``status="error"``. Mensagens de I/O ficam para o nó write.
    """
    if _has_critical_errors(state):
        return {}

    generated_mock = (state.get("generated_mock") or "").strip()
    if not generated_mock:
        return {"errors": [_MSG_EMPTY], "status": "error"}

    parsed_model = state.get("parsed_model") or {}
    if not parsed_model.get("name") or not parsed_model.get("kind"):
        return {"errors": [_MSG_INTERNAL], "status": "error"}

    expected = _model_property_names(parsed_model)
    if expected is None:
        return {"errors": [_MSG_INVALID], "status": "error"}

    kind = parsed_model.get("kind")
    if kind == "enum":
        # Mock de enum é um valor escalar (primeiro membro); só exige conteúdo.
        if "export const" not in generated_mock:
            return {"errors": [_MSG_INVALID], "status": "error"}
        return {"status": "running"}

    actual = _extract_top_level_object_props(generated_mock)
    if actual is None:
        return {"errors": [_MSG_INVALID], "status": "error"}

    missing = expected - actual
    extras = actual - expected
    if missing or extras:
        details: list[str] = [_MSG_INVALID]
        if missing:
            details.append(
                "Propriedades ausentes no mock: " + ", ".join(sorted(missing)) + "."
            )
        if extras:
            details.append(
                "Propriedades extras no mock: " + ", ".join(sorted(extras)) + "."
            )
        return {"errors": details, "status": "error"}

    return {"status": "running"}
