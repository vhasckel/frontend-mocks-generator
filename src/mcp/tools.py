"""Tools MCP de leitura e escrita de arquivos.

Funções de alto nível usadas pelo fluxo do agente (RF02, RF07).
Aplica sandbox de paths (RN02 / SPEC §12) e restrição a ``.ts`` (RN01).
"""

from __future__ import annotations

from pathlib import Path

from src.mcp.client import FilesystemMCPClient
from src.security.validation import (
    MSG_FILE_NOT_FOUND,
    PathOutsideProjectError,
    assert_within_project_root,
    validate_file_size,
)

_client: FilesystemMCPClient | None = None

_TS_SUFFIX = ".ts"

# Alias público (compatível com nós que capturam PathEscapeError).
PathEscapeError = PathOutsideProjectError


class InvalidExtensionError(ValueError):
    """Extensão inválida para a operação (RN01)."""


def get_client() -> FilesystemMCPClient:
    """Retorna o cliente MCP de filesystem (singleton por processo)."""
    global _client
    if _client is None:
        _client = FilesystemMCPClient()
    return _client


def reset_client() -> None:
    """Descarta o cliente em cache (útil em testes / REPL)."""
    global _client
    _client = None


def _resolve_under_root(
    path: str,
    *,
    client: FilesystemMCPClient | None = None,
) -> Path:
    """Resolve o path e garante sandbox em PROJECT_ROOT (RN02)."""
    mcp = client or get_client()
    return assert_within_project_root(path, root=mcp.project_root.resolve())


def _ensure_ts_extension(path: Path, *, operation: str) -> None:
    """Rejeita caminhos cuja extensão não seja ``.ts`` (RN01)."""
    if path.suffix != _TS_SUFFIX:
        raise InvalidExtensionError(
            f"{operation} permitida apenas para arquivos .ts (RN01): {path.name!r}"
        )


def read_file(path: str) -> str:
    """Lê o conteúdo de um arquivo ``.ts`` sob PROJECT_ROOT (RF02, RN01, RN02).

    Args:
        path: Caminho relativo a PROJECT_ROOT ou absoluto.

    Returns:
        Conteúdo do arquivo como string.
    """
    client = get_client()
    target = _resolve_under_root(path, client=client)
    _ensure_ts_extension(target, operation="Leitura")
    if not client.exists(target):
        raise FileNotFoundError(MSG_FILE_NOT_FOUND)
    validate_file_size(target)
    content = client.read_text(target)
    validate_file_size(target, content_length=len(content.encode("utf-8")))
    return content


def write_file(path: str, content: str, overwrite: bool = False) -> dict:
    """Grava um arquivo de mock ``.ts`` (RF07, RN01–RN03 / SPEC §12 Escrita).

    Args:
        path: Destino relativo a PROJECT_ROOT ou absoluto (deve terminar em ``.ts``).
        content: Conteúdo a gravar.
        overwrite: Se False e o destino já existir, não sobrescreve.

    Returns:
        Dict com ``status`` (``ok`` | ``exists``) e ``path`` resolvido.
    """
    client = get_client()
    target = _resolve_under_root(path, client=client)
    _ensure_ts_extension(target, operation="Escrita")
    # Escrita também limitada ao tamanho configurado (SPEC §12).
    validate_file_size(content_length=len(content.encode("utf-8")))

    if client.exists(target) and not overwrite:
        return {"status": "exists", "path": str(target)}

    client.write_text(target, content)
    return {"status": "ok", "path": str(target)}


def file_exists(path: str) -> bool:
    """Verifica se um arquivo existe sob PROJECT_ROOT (RN02)."""
    client = get_client()
    target = _resolve_under_root(path, client=client)
    return client.exists(target)
