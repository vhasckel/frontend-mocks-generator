# T0 — Bootstrap do repositório

## Objetivo

Inicializar o Git (se necessário), criar `.gitignore`, um `README.md` mínimo apontando para a SPEC e garantir que `docs/tasks/` esteja versionado como índice do fluxo.

## Branch

`feature/00-bootstrap`

## Depende de

`main` (estado atual: apenas `docs/SPEC.md` e, se já existir, `docs/tasks/`)

## Arquivos esperados

- `.gitignore`
- `README.md`
- `docs/tasks/README.md` (já pode existir; manter/alinhar se necessário)
- Demais arquivos desta pasta `docs/tasks/*.md` devem permanecer versionados

## Critérios de aceite da etapa

- [ ] Repositório Git inicializado com branch `main`
- [ ] `.gitignore` cobre `.env`, `.venv`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `dist/`, `*.egg-info/`
- [ ] `README.md` descreve o projeto em 2–4 frases e aponta para `docs/SPEC.md` e `docs/tasks/`
- [ ] Nenhum código de agente Python ainda (isso é T1+)

## Commits sugeridos

1. `chore: initialize repository and gitignore`
2. `docs: add task flow index and SPEC pointer`

## Prompt

```
Você está implementando a etapa T0 do projeto frontend-mocks-generator.

Contexto do projeto: leia docs/SPEC.md e docs/tasks/README.md. Esta etapa NÃO implementa o agente — apenas bootstrap.

Objetivo:
1. Se o Git ainda não estiver inicializado, rode `git init` e garanta a branch `main`.
2. Crie a branch `feature/00-bootstrap` a partir de `main`.
3. Crie/atualize `.gitignore` cobrindo: `.env`, `.venv/`, `venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `dist/`, `build/`, `*.egg-info/`, `.idea/`, `.vscode/` (opcional), e arquivos de OS (`.DS_Store`).
4. Crie/atualize `README.md` na raiz: título "Frontend Mocks Generator", resumo curto do objetivo (agente LangGraph + MCP que gera mocks TypeScript a partir de models), e links/pointers para `docs/SPEC.md` e `docs/tasks/` (fluxo de implementação).
5. Se `docs/tasks/` já existir com os arquivos de tarefa, mantenha-os intactos; se faltar o índice, alinhe com o conteúdo esperado em docs/tasks/README.md.
6. NÃO crie pyproject.toml, src/, mcp tools, LangGraph, CLI ou .env.example nesta etapa.
7. Faça EXATAMENTE estes commits (mensagens literais), via HEREDOC, apenas quando o usuário pedir commit OU se o fluxo da tarefa pedir commits — neste prompt, CRIAR os commits ao final:
   - `chore: initialize repository and gitignore`
   - `docs: add task flow index and SPEC pointer`
8. Ao final, resuma arquivos alterados e como validar: `git status`, `git log --oneline -5`, confirmar que SPEC e tasks estão rastreados.

Regras: não edite docs/SPEC.md; não antecipe T1+; commits objetivos e pequenos.
```
