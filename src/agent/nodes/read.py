"""Nó de leitura do arquivo TypeScript via MCP (RF01, RF02, RN01)."""

from __future__ import annotations

from src.agent.state import MockAgentState
from src.mcp import tools as mcp_tools
from src.security.validation import (
    MSG_FILE_NOT_FOUND,
    MSG_INTERNAL,
    MSG_INVALID_TS,
    PathOutsideProjectError,
    ValidationError,
    validate_file_size,
    validate_input_path,
)


def read_node(state: MockAgentState) -> dict:
    """Lê o arquivo de entrada via tools MCP e preenche ``source_code``.

    Valida presença de ``input_path``, existência no filesystem, extensão
    ``.ts`` e tamanho (``MAX_FILE_SIZE_BYTES``). Em falha, retorna ``errors``
    com mensagens da SPEC §13 e ``status="error"``. Em sucesso, retorna
    ``source_code`` e ``status="running"``.
    """
    input_path = (state.get("input_path") or "").strip()

    try:
        resolved = validate_input_path(input_path)
        validate_file_size(resolved)
        source_code = mcp_tools.read_file(str(resolved))
    except ValidationError as exc:
        return {"errors": [exc.message], "status": "error"}
    except mcp_tools.InvalidExtensionError:
        return {"errors": [MSG_INVALID_TS], "status": "error"}
    except FileNotFoundError:
        return {"errors": [MSG_FILE_NOT_FOUND], "status": "error"}
    except PathOutsideProjectError:
        return {"errors": [MSG_INTERNAL], "status": "error"}
    except Exception:
        return {"errors": [MSG_INTERNAL], "status": "error"}

    return {"source_code": source_code, "status": "running"}
