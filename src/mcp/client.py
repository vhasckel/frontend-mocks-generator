"""Cliente MCP de filesystem para o agente.

Toda interação do agente com o sistema de arquivos passa por esta camada MCP
(RNF03, RF02, RF07) — leitura de models e escrita de mocks.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


class FilesystemMCPClient:
    """Abstração MCP de filesystem usada pelo agente.

    Expõe operações de baixo nível (`read_text`, `write_text`, `exists`)
    consumidas pelas tools em ``src.mcp.tools``. Em vez de subir um servidor
    MCP externo nesta etapa, esta classe encapsula o contrato filesystem do
    protocolo MCP no processo do agente.
    """

    def __init__(
        self,
        project_root: str | Path | None = None,
        mocks_output_dir: str | Path | None = None,
    ) -> None:
        load_dotenv()

        root = project_root if project_root is not None else os.getenv("PROJECT_ROOT", ".")
        self.project_root = Path(root).expanduser().resolve()

        mocks = (
            mocks_output_dir
            if mocks_output_dir is not None
            else os.getenv("MOCKS_OUTPUT_DIR", "examples/mocks")
        )
        mocks_path = Path(mocks).expanduser()
        if not mocks_path.is_absolute():
            mocks_path = self.project_root / mocks_path
        self.mocks_output_dir = mocks_path.resolve()

    def read_text(self, path: Path) -> str:
        """Lê o conteúdo de um arquivo como texto UTF-8."""
        return path.read_text(encoding="utf-8")

    def write_text(self, path: Path, content: str) -> None:
        """Grava conteúdo em um arquivo, criando diretórios pais se preciso."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def exists(self, path: Path) -> bool:
        """Retorna True se o caminho existir no filesystem."""
        return path.exists()
