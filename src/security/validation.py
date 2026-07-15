"""Validações de segurança e entrada (SPEC §12, RN01–RN03).

Mensagens de erro centralizadas com os textos EXATOS da SPEC §13.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Mensagens EXATAS — SPEC §13
# ---------------------------------------------------------------------------

MSG_FILE_NOT_FOUND = "Arquivo não encontrado."
MSG_INVALID_TS = "O arquivo informado não é um arquivo TypeScript válido."
MSG_NO_INTERFACE = "Nenhuma interface exportada foi encontrada."
MSG_WRITE_FAIL = "Não foi possível criar o arquivo de mock."
MSG_INTERNAL = "Erro interno durante a geração do mock."

# Mensagem clara para API key ausente (SPEC §12 API Keys) — nunca incluir o valor.
MSG_MISSING_API_KEY = (
    "GOOGLE_API_KEY não configurada. Defina a variável de ambiente para continuar."
)

_TS_SUFFIX = ".ts"
_DEFAULT_MAX_FILE_SIZE_BYTES = 100_000


class ValidationError(Exception):
    """Falha de validação com mensagem pronta para o usuário (SPEC §13)."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class PathOutsideProjectError(PermissionError):
    """Path resolvido escapa de PROJECT_ROOT (RN02 / SPEC §12 Escrita)."""


def get_project_root() -> Path:
    """Retorna ``PROJECT_ROOT`` resolvido (env ou ``.``)."""
    load_dotenv()
    root = os.getenv("PROJECT_ROOT", ".")
    return Path(root).expanduser().resolve()


def get_max_file_size_bytes() -> int:
    """Limite de tamanho configurado em ``MAX_FILE_SIZE_BYTES``."""
    load_dotenv()
    raw = os.getenv("MAX_FILE_SIZE_BYTES", str(_DEFAULT_MAX_FILE_SIZE_BYTES))
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return _DEFAULT_MAX_FILE_SIZE_BYTES
    return value if value > 0 else _DEFAULT_MAX_FILE_SIZE_BYTES


def assert_within_project_root(
    path: str | Path,
    *,
    root: Path | None = None,
) -> Path:
    """Normaliza ``path`` e garante que permanece sob PROJECT_ROOT (RN02).

    Returns:
        Path absoluto resolvido dentro do root.

    Raises:
        PathOutsideProjectError: se o destino final escapar do root.
    """
    project_root = (root if root is not None else get_project_root()).resolve()

    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = project_root / candidate

    # resolve() normaliza ``..`` e segue symlinks; o alvo final deve
    # permanecer sob PROJECT_ROOT.
    resolved = candidate.resolve()
    try:
        resolved.relative_to(project_root)
    except ValueError as exc:
        raise PathOutsideProjectError(
            f"Escrita/leitura fora de PROJECT_ROOT bloqueada (RN02): {path!r} "
            f"resolve para {resolved} (root={project_root})"
        ) from exc
    return resolved


def validate_input_path(path: str) -> Path:
    """Valida path de entrada: extensão ``.ts``, normalização e existência.

    Returns:
        Path absoluto resolvido sob PROJECT_ROOT.

    Raises:
        ValidationError: com mensagens da SPEC §13 (arquivo inexistente / inválido).
        PathOutsideProjectError: path fora do projeto (RN02).
    """
    raw = (path or "").strip()
    if not raw:
        raise ValidationError(MSG_FILE_NOT_FOUND)

    # RN01 — somente .ts (checagem cedo, antes de I/O).
    if Path(raw).suffix != _TS_SUFFIX:
        raise ValidationError(MSG_INVALID_TS)

    resolved = assert_within_project_root(raw)

    if resolved.suffix != _TS_SUFFIX:
        raise ValidationError(MSG_INVALID_TS)

    if not resolved.is_file():
        raise ValidationError(MSG_FILE_NOT_FOUND)

    return resolved


def validate_file_size(
    path: str | Path | None = None,
    *,
    content_length: int | None = None,
) -> None:
    """Garante que o arquivo/conteúdo respeita ``MAX_FILE_SIZE_BYTES`` (SPEC §12).

    Aceita um path em disco e/ou o tamanho já conhecido em bytes.
    Ultrapassar o limite é tratado como erro interno (SPEC §13).

    Raises:
        ValidationError: se o tamanho exceder o limite.
        ValidationError: se ``path`` e ``content_length`` forem ambos omitidos.
    """
    max_bytes = get_max_file_size_bytes()
    size: int | None = content_length

    if path is not None:
        target = Path(path)
        if target.is_file():
            disk_size = target.stat().st_size
            size = disk_size if size is None else max(size, disk_size)

    if size is None:
        raise ValidationError(MSG_INTERNAL)

    if size > max_bytes:
        raise ValidationError(MSG_INTERNAL)
