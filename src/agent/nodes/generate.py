"""Nó de geração do mock TypeScript (RF05, RF06, RN04–RN06, SPEC §11)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from src.agent.state import MockAgentState
from src.rules import generation as rules

_MSG_INTERNAL = "Erro interno durante a geração do mock."


def _has_critical_errors(state: MockAgentState) -> bool:
    if state.get("status") == "error":
        return True
    errors = state.get("errors") or []
    return len(errors) > 0


def _mocks_output_dir() -> Path:
    load_dotenv()
    root = Path(os.getenv("PROJECT_ROOT", ".")).expanduser()
    mocks = Path(os.getenv("MOCKS_OUTPUT_DIR", "examples/mocks")).expanduser()
    if not mocks.is_absolute():
        mocks = root / mocks
    return mocks


def generate_node(state: MockAgentState) -> dict:
    """Gera ``generated_mock`` e ``output_path`` a partir de ``parsed_model``.

    Usa as regras de ``src.rules.generation`` (SPEC §11). Não inventa
    propriedades além das do modelo (RN04/RN05) e respeita tipos (RN06).
    Short-circuit se já houver erros críticos ou se ``parsed_model`` estiver
    ausente/ incompleto.
    """
    if _has_critical_errors(state):
        return {}

    parsed_model = state.get("parsed_model") or {}
    entity_name = parsed_model.get("name")
    kind = parsed_model.get("kind")
    if not entity_name or not kind:
        return {"errors": [_MSG_INTERNAL], "status": "error"}

    try:
        output_path = rules.resolve_output_path(str(entity_name), _mocks_output_dir())
        # Prefer path relative to PROJECT_ROOT when possible (stable, portable).
        load_dotenv()
        project_root = Path(os.getenv("PROJECT_ROOT", ".")).expanduser().resolve()
        try:
            output_path_str = str(Path(output_path).resolve().relative_to(project_root))
        except ValueError:
            output_path_str = str(output_path)

        input_path = (state.get("input_path") or "").strip()
        generated_mock = rules.generate_mock_code(
            parsed_model,
            input_path=input_path,
            output_path=output_path_str,
        )
    except Exception:
        return {"errors": [_MSG_INTERNAL], "status": "error"}

    if not generated_mock.strip():
        return {"errors": [_MSG_INTERNAL], "status": "error"}

    return {
        "generated_mock": generated_mock,
        "output_path": output_path_str,
        "status": "running",
    }
