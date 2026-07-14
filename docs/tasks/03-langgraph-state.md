# T3 — Estado compartilhado LangGraph

## Objetivo

Definir o estado do agente (`MockAgentState`) compartilhado entre nós (RNF01, RNF02).

## Branch

`feature/03-langgraph-state`

## Depende de

`feature/02-mcp-filesystem` já mergeada em `main`

## Arquivos esperados

```
src/agent/state.py
```

## Critérios de aceite da etapa

- [ ] `MockAgentState` tipado (TypedDict e/ou modelo Pydantic alinhado ao uso com LangGraph)
- [ ] Campos míninos: `input_path`, `source_code`, `parsed_model`, `generated_mock`, `output_path`, `errors`, `warnings`, `status`
- [ ] Documentação inline dos campos e valores possíveis de `status` (ex.: `pending`, `ok`, `error`)
- [ ] Sem implementação de nodes/graph ainda

## Commits sugeridos

1. `feat: define shared LangGraph agent state`

## Prompt

```
Você está implementando a etapa T3 do projeto frontend-mocks-generator.

Pré-requisito: `feature/02-mcp-filesystem` mergeada em `main`. Leia docs/SPEC.md (fluxo seção 7, RNF01, RNF02) e docs/tasks/README.md (estrutura alvo).

Objetivo:
1. `git checkout main`. Crie `feature/03-langgraph-state`.
2. Crie `src/agent/state.py` com o estado compartilhado do LangGraph, por exemplo:

   MockAgentState (TypedDict total=False ou schema recomendado pelo LangGraph atual) contendo:
   - input_path: str          # caminho do .ts de entrada (RF01)
   - source_code: str         # conteúdo lido via MCP
   - parsed_model: dict       # estrutura interpretada (nome, kind: interface|type|enum, properties...)
   - generated_mock: str      # código TypeScript do mock
   - output_path: str         # caminho do arquivo de saída
   - errors: list[str]        # mensagens de erro (seção 13)
   - warnings: list[str]      # avisos (ex.: mock já existe)
   - status: str              # pending | running | success | error (escolha um conjunto coerente e documente)

3. Exporte helpers opcionais se úteis: `initial_state(input_path: str) -> MockAgentState`.
4. NÃO implemente nodes, graph.py, CLI ou chamadas à LLM.
5. Commit literal:
   - `feat: define shared LangGraph agent state`
6. Ao final: mostre o shape do estado e como os próximos nós (T4+) devem atualizar campos.

Alinhamento SPEC: RNF01, RNF02; prepara RF01–RF08 sem implementá-los ainda.
```
