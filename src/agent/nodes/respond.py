"""Nó de resposta ao usuário (RF08, SPEC §13)."""

from __future__ import annotations

from src.agent.state import MockAgentState
from src.security.validation import MSG_INTERNAL


def respond_node(state: MockAgentState) -> dict:
    """Monta ``message`` final de sucesso ou agrega ``errors``/``warnings``.

    Sucesso: informa o caminho do mock criado. Erro: junta as mensagens
    acumuladas em ``errors`` (e ``warnings`` quando presentes). Se o status
    for ``error`` sem mensagens mapeadas, usa a mensagem de erro inesperado
    da SPEC §13.
    """
    errors = list(state.get("errors") or [])
    warnings = list(state.get("warnings") or [])
    status = state.get("status")
    output_path = (state.get("output_path") or "").strip()

    if status == "success" and not errors:
        message = f"Mock gerado com sucesso em {output_path}."
        if warnings:
            message = message + " " + " ".join(warnings)
        return {"message": message, "status": "success"}

    parts: list[str] = []
    if errors:
        parts.extend(errors)
    if warnings:
        parts.extend(warnings)

    if parts:
        return {"message": " ".join(parts), "status": "error"}

    return {"message": MSG_INTERNAL, "status": "error"}
