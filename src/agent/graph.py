"""Grafo LangGraph do Frontend Mocks Generator (SPEC §7).

Fluxo feliz:
  START → read → interpret → generate → validate → write → respond → END

Em qualquer nó com ``status=error`` ou ``errors`` não vazios, o fluxo
encurta para ``respond`` e termina (sem geração/escrita posteriores).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from langgraph.graph import END, START, StateGraph

from src.agent.nodes.generate import generate_node
from src.agent.nodes.interpret import interpret_node
from src.agent.nodes.read import read_node
from src.agent.nodes.respond import respond_node
from src.agent.nodes.validate import validate_node
from src.agent.nodes.write import write_node
from src.agent.state import MockAgentState, initial_state

RouteTarget = Literal[
    "interpret",
    "generate",
    "validate",
    "write",
    "respond",
]


def _has_failure(state: MockAgentState) -> bool:
    """Convenção dos nós: falha se ``status=error`` ou ``errors`` não vazio."""
    if state.get("status") == "error":
        return True
    errors = state.get("errors") or []
    return len(errors) > 0


def _route_after(next_node: RouteTarget) -> Callable[[MockAgentState], RouteTarget]:
    """Fábrica de roteadores condicionais: falha → respond; senão → next_node."""

    def _route(state: MockAgentState) -> RouteTarget:
        if _has_failure(state):
            return "respond"
        return next_node

    return _route


def build_graph():
    """Compila o StateGraph com os nós do fluxo (RNF01, RF01–RF08)."""
    graph = StateGraph(MockAgentState)

    graph.add_node("read", read_node)
    graph.add_node("interpret", interpret_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)
    graph.add_node("write", write_node)
    graph.add_node("respond", respond_node)

    graph.add_edge(START, "read")
    graph.add_conditional_edges(
        "read",
        _route_after("interpret"),
        {"interpret": "interpret", "respond": "respond"},
    )
    graph.add_conditional_edges(
        "interpret",
        _route_after("generate"),
        {"generate": "generate", "respond": "respond"},
    )
    graph.add_conditional_edges(
        "generate",
        _route_after("validate"),
        {"validate": "validate", "respond": "respond"},
    )
    graph.add_conditional_edges(
        "validate",
        _route_after("write"),
        {"write": "write", "respond": "respond"},
    )
    # write → respond sempre (sucesso ou falha de I/O / arquivo existente)
    graph.add_edge("write", "respond")
    graph.add_edge("respond", END)

    return graph.compile()


def run_agent(input_path: str) -> MockAgentState:
    """Executa o fluxo completo a partir do path do arquivo TypeScript."""
    app = build_graph()
    result = app.invoke(initial_state(input_path))
    return result  # type: ignore[return-value]
