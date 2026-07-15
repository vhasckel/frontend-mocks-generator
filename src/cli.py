"""CLI do Frontend Mocks Generator (RNF01, RF01, RF08).

Uso::

    python -m src.cli <arquivo.ts>
"""

from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

from src.agent.graph import run_agent


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.cli",
        description=(
            "Gera um arquivo de mock TypeScript a partir de uma interface/type."
        ),
    )
    parser.add_argument(
        "input_path",
        help="Caminho do arquivo TypeScript de entrada (ex.: examples/types/User.ts)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada da CLI. Retorna exit code (0 sucesso, !=0 falha)."""
    load_dotenv()
    parser = _build_parser()
    args = parser.parse_args(argv)

    result = run_agent(args.input_path)
    message = (result.get("message") or "").strip()
    status = result.get("status")
    errors = result.get("errors") or []

    if message:
        print(message)
    elif errors:
        print(" ".join(errors))
    else:
        print("Erro interno durante a geração do mock.")

    if status == "success" and not errors:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
