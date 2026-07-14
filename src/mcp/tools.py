"""Tools MCP de leitura e escrita de arquivos.

Funções de alto nível usadas pelo fluxo do agente (RF02, RF07).
"""

from __future__ import annotations

from pathlib import Path

from src.mcp.client import FilesystemMCPClient

_client: FilesystemMCPClient | None = None


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


def _resolve_path(path: str, *, client: FilesystemMCPClient | None = None) -> Path:
    """Resolve um path relativo ou absoluto a partir de PROJECT_ROOT."""
    mcp = client or get_client()
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = mcp.project_root / candidate
    return candidate.resolve()


def read_file(path: str) -> str:
    """Lê o conteúdo de um arquivo sob PROJECT_ROOT (RF02).

    Args:
        path: Caminho relativo a PROJECT_ROOT ou absoluto.

    Returns:
        Conteúdo do arquivo como string.
    """
    client = get_client()
    target = _resolve_path(path, client=client)
    if not client.exists(target):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return client.read_text(target)


def write_file(path: str, content: str, overwrite: bool = False) -> dict:
    """Grava um arquivo de mock (RF07, RN03 / SPEC §12 Escrita).

    Args:
        path: Destino relativo a PROJECT_ROOT ou absoluto.
        content: Conteúdo a gravar.
        overwrite: Se False e o destino já existir, não sobrescreve.

    Returns:
        Dict com ``status`` (``ok`` | ``exists``) e ``path`` resolvido.
    """
    client = get_client()
    target = _resolve_path(path, client=client)

    if client.exists(target) and not overwrite:
        return {"status": "exists", "path": str(target)}

    client.write_text(target, content)
    return {"status": "ok", "path": str(target)}


def file_exists(path: str) -> bool:
    """Verifica se um arquivo existe sob PROJECT_ROOT."""
    client = get_client()
    target = _resolve_path(path, client=client)
    return client.exists(target)
