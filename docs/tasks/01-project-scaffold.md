# T1 — Scaffold do projeto Python

## Objetivo

Criar a base Python 3.11+, dependências (LangGraph, LangChain, MCP, OpenAI, dotenv) e a árvore de pacotes vazia alinhada à SPEC (RNF04).

## Branch

`feature/01-project-scaffold`

## Depende de

`feature/00-bootstrap` já mergeada em `main`

## Arquivos esperados

```
pyproject.toml
requirements.txt
.env.example
src/__init__.py
src/agent/__init__.py
src/agent/nodes/__init__.py
src/mcp/__init__.py
src/rules/__init__.py
src/security/__init__.py
examples/types/.gitkeep
examples/mocks/.gitkeep
```

## Critérios de aceite da etapa

- [ ] Python ≥ 3.11 declarado em `pyproject.toml`
- [ ] Dependências: `langgraph`, `langchain`, `langchain-openai`, `mcp`, `python-dotenv` (versões razoáveis/pinadas ou ranges estáveis)
- [ ] `.env.example` com `OPENAI_API_KEY=` e variáveis de caminho permitido (ex.: `PROJECT_ROOT=`, `MOCKS_OUTPUT_DIR=examples/mocks`)
- [ ] Pacotes vazios com `__init__.py` nas pastas `src/agent`, `src/agent/nodes`, `src/mcp`, `src/rules`, `src/security`
- [ ] Nenhum nó LangGraph, tool MCP ou CLI implementados ainda

## Commits sugeridos

1. `chore: add Python project dependencies and layout`
2. `docs: add env example for API keys`

## Prompt

```
Você está implementando a etapa T1 do projeto frontend-mocks-generator.

Pré-requisito: `feature/00-bootstrap` já está mergeada em `main`. Leia docs/SPEC.md (seção 17 — tecnologias) e docs/tasks/README.md.

Objetivo:
1. `git checkout main && git pull` (se houver remote). Crie a branch `feature/01-project-scaffold`.
2. Crie `pyproject.toml` para um pacote instalável local (nome sugerido: `frontend-mocks-generator` ou `fmg`), Python >=3.11, com dependências:
   - langgraph
   - langchain
   - langchain-openai
   - mcp
   - python-dotenv
   Inclua também `requirements.txt` gerado/espelhado para instalação simples (`pip install -r requirements.txt`).
3. Crie a estrutura de pacotes (somente `__init__.py` vazios ou com docstring mínima — SEM lógica):
   src/
     __init__.py
     agent/__init__.py
     agent/nodes/__init__.py
     mcp/__init__.py
     rules/__init__.py
     security/__init__.py
   examples/types/.gitkeep
   examples/mocks/.gitkeep
4. Crie `.env.example` (NUNCA commit `.env`) com:
   OPENAI_API_KEY=
   PROJECT_ROOT=.
   MOCKS_OUTPUT_DIR=examples/mocks
   MAX_FILE_SIZE_BYTES=100000
   Comentário curto lembrando que API keys não vão no código (SPEC seção 12).
5. Atualize o README.md da raiz apenas com instruções mínimas de setup: criar venv, instalar deps, copiar .env.example → .env. Não escreva TECHNICAL.md (isso é T9).
6. NÃO implemente client MCP, state LangGraph, nodes, graph, cli.py ou rules de geração nesta etapa.
7. Commits literais (HEREDOC):
   - `chore: add Python project dependencies and layout`
   - `docs: add env example for API keys`
8. Ao final: listar arquivos criados e validação manual (`ls -R src examples`, conferir pyproject/requirements/.env.example).

Alinhamento SPEC: RNF04 (módulos), seção 12 (API keys em env), seção 17 (stack).
```
