"""Estado compartilhado do agente LangGraph (RNF01, RNF02).

Os nós (T4+) leem este estado e retornam updates parciais; o LangGraph
mergeia no estado global. Listas `errors` e `warnings` usam reducer
`operator.add` para acumular mensagens entre nós.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, Literal, TypedDict

# Status do fluxo do agente (campo `status`):
# - pending: estado inicial, antes de qualquer nó executar
# - running: fluxo em andamento (leitura / interpretação / geração / etc.)
# - success: mock gerado e persistido com sucesso
# - error: falha tratada; detalhes em `errors` (SPEC §13)
AgentStatus = Literal["pending", "running", "success", "error"]


class MockAgentState(TypedDict, total=False):
    """Schema do estado compartilhado entre os nós do grafo.

    Campos:
        input_path: caminho do arquivo TypeScript de entrada (RF01).
        source_code: conteúdo lido via MCP (RF02).
        parsed_model: estrutura interpretada pelo LLM, tipicamente com
            chaves como ``name``, ``kind`` (``interface`` | ``type`` | ``enum``),
            ``properties``, valores de enum, etc. (RF03–RF04).
        generated_mock: código TypeScript do mock gerado (RF05–RF06).
        output_path: caminho do arquivo de mock a escrever (RF07).
        errors: mensagens de erro acumuladas (SPEC §13).
        warnings: avisos não fatais (ex.: mock já existe — RN03).
        status: ``pending`` | ``running`` | ``success`` | ``error``.
    """

    input_path: str
    source_code: str
    parsed_model: dict[str, Any]
    generated_mock: str
    output_path: str
    errors: Annotated[list[str], operator.add]
    warnings: Annotated[list[str], operator.add]
    status: AgentStatus


def initial_state(input_path: str) -> MockAgentState:
    """Cria o estado inicial com ``input_path`` e defaults seguros."""
    return {
        "input_path": input_path,
        "source_code": "",
        "parsed_model": {},
        "generated_mock": "",
        "output_path": "",
        "errors": [],
        "warnings": [],
        "status": "pending",
    }
