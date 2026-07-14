"""Tools MCP de leitura e escrita de arquivos.

Funções de alto nível usadas pelo fluxo do agente (RF02, RF07).
Aplica sandbox de paths (RN02 / SPEC §12) e restrição a ``.ts`` (RN01).
"""

from __future__ import annotations

from pathlib import Path

from src.mcp.client import FilesystemMCPClient

_client: FilesystemMCPClient | None = None

_TS_SUFFIX = ".ts"


class PathEscapeError(PermissionError):
    """Path resolvido escapa de PROJECT_ROOT (RN02)."""


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


def _is_under_root(path: Path, root: Path) -> bool:
    """True se ``path`` (já resolvido) permanece dentro de ``root``."""
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _resolve_under_root(
    path: str,
    *,
    client: FilesystemMCPClient | None = None,
) -> Path:
    """Resolve o path com ``Path.resolve()`` e garante sandbox em PROJECT_ROOT.

    Bloqueia ``..`` e symlinks cujo alvo final escape do root (RN02).
    """
    mcp = client or get_client()
    root = mcp.project_root.resolve()

    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate

    # resolve() normaliza ``..`` e segue symlinks; o destino final deve
    # permanecer sob PROJECT_ROOT.
    resolved = candidate.resolve()
    if not _is_under_root(resolved, root):
        raise PathEscapeError(
            f"Escrita/leitura fora de PROJECT_ROOT bloqueada (RN02): {path!r} "
            f"resolve para {resolved} (root={root})"
        )
    return resolved


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
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return client.read_text(target)


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

    if client.exists(target) and not overwrite:
        return {"status": "exists", "path": str(target)}

    client.write_text(target, content)
    return {"status": "ok", "path": str(target)}


def file_exists(path: str) -> bool:
    """Verifica se um arquivo existe sob PROJECT_ROOT (RN02)."""
    client = get_client()
    target = _resolve_under_root(path, client=client)
    return client.exists(target)
