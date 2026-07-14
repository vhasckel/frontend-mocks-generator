"""Nó de leitura do arquivo TypeScript via MCP (RF01, RF02, RN01)."""

from __future__ import annotations

from pathlib import Path

from src.agent.state import MockAgentState
from src.mcp import tools as mcp_tools

_MSG_NOT_FOUND = "Arquivo não encontrado."
_MSG_INVALID_TS = "O arquivo informado não é um arquivo TypeScript válido."
_MSG_INTERNAL = "Erro interno durante a geração do mock."


def read_node(state: MockAgentState) -> dict:
    """Lê o arquivo de entrada via tools MCP e preenche ``source_code``.

    Valida presença de ``input_path``, existência no filesystem e extensão
    ``.ts``. Em falha, retorna ``errors`` com mensagens da SPEC §13 e
    ``status="error"``. Em sucesso, retorna ``source_code`` e
    ``status="running"``.
    """
    input_path = (state.get("input_path") or "").strip()
    if not input_path:
        return {"errors": [_MSG_NOT_FOUND], "status": "error"}

    if Path(input_path).suffix != ".ts":
        return {"errors": [_MSG_INVALID_TS], "status": "error"}

    try:
        if not mcp_tools.file_exists(input_path):
            return {"errors": [_MSG_NOT_FOUND], "status": "error"}
        source_code = mcp_tools.read_file(input_path)
    except mcp_tools.InvalidExtensionError:
        return {"errors": [_MSG_INVALID_TS], "status": "error"}
    except FileNotFoundError:
        return {"errors": [_MSG_NOT_FOUND], "status": "error"}
    except Exception:
        return {"errors": [_MSG_INTERNAL], "status": "error"}

    return {"source_code": source_code, "status": "running"}
