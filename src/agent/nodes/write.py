"""Nó de escrita do mock via MCP (RF07, RN02, RN03, SPEC §12–§13)."""

from __future__ import annotations

from src.agent.state import MockAgentState
from src.mcp import tools as mcp_tools

_MSG_WRITE_FAIL = "Não foi possível criar o arquivo de mock."


def _has_critical_errors(state: MockAgentState) -> bool:
    if state.get("status") == "error":
        return True
    errors = state.get("errors") or []
    return len(errors) > 0


def write_node(state: MockAgentState) -> dict:
    """Persiste ``generated_mock`` em ``output_path`` via tools MCP.

    Short-circuit se validação falhou, ``status`` já for ``error`` ou
    ``generated_mock`` estiver ausente. Usa ``overwrite=False`` (RN03 / SPEC
    §12): se o destino existir, informa o usuário via ``warnings`` sem
    sobrescrever. Falhas de permissão/IO → mensagem da SPEC §13.
    """
    if _has_critical_errors(state):
        return {}

    generated_mock = state.get("generated_mock") or ""
    if not generated_mock.strip():
        return {}

    output_path = (state.get("output_path") or "").strip()
    if not output_path:
        return {"errors": [_MSG_WRITE_FAIL], "status": "error"}

    try:
        result = mcp_tools.write_file(
            output_path,
            generated_mock,
            overwrite=False,
        )
    except (PermissionError, OSError, mcp_tools.InvalidExtensionError):
        return {"errors": [_MSG_WRITE_FAIL], "status": "error"}
    except Exception:
        return {"errors": [_MSG_WRITE_FAIL], "status": "error"}

    if result.get("status") == "exists":
        existing = result.get("path") or output_path
        return {
            "warnings": [
                f"O arquivo de mock já existe: {existing}. "
                "Não foi sobrescrito."
            ],
            "status": "error",
        }

    return {
        "output_path": result.get("path") or output_path,
        "status": "success",
    }
