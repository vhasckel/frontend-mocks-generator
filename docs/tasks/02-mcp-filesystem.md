# T2 — Tools MCP de filesystem

## Objetivo

Implementar cliente MCP e tools de leitura/escrita com sandbox de paths, restrição a `.ts` e detecção de arquivo já existente (RF02, RF07, RN01–RN03, RNF03).

## Branch

`feature/02-mcp-filesystem`

## Depende de

`feature/01-project-scaffold` já mergeada em `main`

## Arquivos esperados

```
src/mcp/client.py
src/mcp/tools.py
```

(Opcional: helpers pequenos sob `src/security/` **somente** se necessários para path/extensão nesta etapa; validação completa fica em T8.)

## Critérios de aceite da etapa

- [ ] É possível ler conteúdo de um arquivo `.ts` existente via API das tools
- [ ] Escrita só permite extensão `.ts` (RN01)
- [ ] Escrita fora de `PROJECT_ROOT` é rejeitada (RN02)
- [ ] Se o destino do mock já existir, a tool sinaliza (não sobrescreve silenciosamente) (RN03)
- [ ] Sem nós LangGraph nesta etapa

## Commits sugeridos

1. `feat: add MCP filesystem read and write tools`
2. `feat: enforce path sandbox and ts-only writes`

## Prompt

```
Você está implementando a etapa T2 do projeto frontend-mocks-generator.

Pré-requisito: `feature/01-project-scaffold` mergeada em `main`. Leia docs/SPEC.md (RF02, RF07, RN01–RN03, seção 12 Escrita) e docs/tasks/README.md.

Objetivo:
1. `git checkout main` (pull se houver remote). Crie `feature/02-mcp-filesystem`.
2. Implemente `src/mcp/client.py`: inicialização/conexão com servidor ou camada MCP de filesystem adequada ao ecossistema Python `mcp`. Se um servidor MCP completo exigir setup pesado, encapsule uma abstração `FilesystemMCPClient` que:
   - expose operações usadas pelo agente (`read_text`, `write_text`, `exists`)
   - documente no docstring que a interação filesystem do agente passa por esta camada MCP (RNF03)
   - carregue `PROJECT_ROOT` e `MOCKS_OUTPUT_DIR` de variáveis de ambiente (python-dotenv)
3. Implemente `src/mcp/tools.py` com funções/tools claras:
   - `read_file(path: str) -> str` — lê arquivo sob PROJECT_ROOT
   - `write_file(path: str, content: str, overwrite: bool = False) -> dict` — grava mock
   - `file_exists(path: str) -> bool`
4. Regras obrigatórias:
   - Aceitar leitura preferencialmente de `.ts`; rejeitar escrita que não seja `.ts` (RN01) com erro claro
   - Resolver paths com `Path.resolve()` e garantir que o destino final permanece dentro de PROJECT_ROOT (RN02) — bloquear `..` e symlinks que escapem
   - Se arquivo destino existir e `overwrite=False`, NÃO sobrescrever; retornar sinalização (ex.: status `exists`) (RN03 / seção 12)
5. NÃO implemente LangGraph state, nodes, generation rules ou CLI.
6. Commits literais:
   - `feat: add MCP filesystem read and write tools`
   - `feat: enforce path sandbox and ts-only writes`
7. Ao final: explique como validar manualmente com um script curto ou REPL (ler um arquivo de teste sob examples/, tentativa de write fora do root deve falhar).

Alinhamento SPEC: RF02, RF07, RN01, RN02, RN03, RNF03, seção 12.
```
