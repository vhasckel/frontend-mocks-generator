# T7 — Grafo LangGraph + CLI + exemplos

## Objetivo

Orquestrar o fluxo completo (seção 7), expor CLI e adicionar exemplos TypeScript (RNF01, RF01, RF08).

## Branch

`feature/07-graph-cli`

## Depende de

`feature/06-nodes-write-response` já mergeada em `main`

## Arquivos esperados

```
src/agent/graph.py
src/cli.py
examples/types/User.ts
examples/types/AddressUser.ts   # opcional: objeto aninhado (caso 2)
```

## Critérios de aceite da etapa

- [ ] Grafo: START → read → interpret → generate → validate → write → respond → END
- [ ] Arestas condicionais para short-circuit em `status=error` / errors (ir para respond)
- [ ] CLI: `python -m src.cli <path-to.ts>` imprime a mensagem final
- [ ] Exemplo `examples/types/User.ts` conforme SPEC seção 5
- [ ] Smoke test documentado: gerar mock sob `examples/mocks/`

## Commits sugeridos

1. `feat: wire LangGraph flow end to end`
2. `feat: add CLI entrypoint`
3. `chore: add sample TypeScript types`

## Prompt

```
Você está implementando a etapa T7 do projeto frontend-mocks-generator.

Pré-requisito: `feature/06-nodes-write-response` mergeada em `main`. Leia docs/SPEC.md (seção 7 Fluxo Geral, critérios §15 primeiros itens, casos de uso §14) e docs/tasks/README.md.

Objetivo:
1. `git checkout main`. Crie `feature/07-graph-cli`.
2. Implemente `src/agent/graph.py`:
   - StateGraph com MockAgentState
   - Nós: read, interpret, generate, validate, write, respond (importar de src/agent/nodes/*)
   - Fluxo feliz: read → interpret → generate → validate → write → respond
   - Em qualquer nó que deixe status=error (ou errors não vazios, conforme convenção já usada), rotear para respond e encerrar (não continuar geração/escrita)
   - Função `build_graph()` / `run_agent(input_path: str) -> MockAgentState` (ou dict com message)
3. Implemente `src/cli.py` e garanta invocação `python -m src.cli <arquivo.ts>`:
   - argparse ou sys.argv
   - carregar dotenv
   - chamar run_agent
   - print da message / erros com exit code != 0 em falha
   - Pode precisar de src/__main__.py ou pacote configurado — escolha o padrão mínimo que funcione
4. Adicione examples:
   - examples/types/User.ts (interface User id/name/email/active como na SPEC)
   - Opcional: examples/types com Address aninhado (caso 2)
5. NÃO foque ainda em harden completo de security (T8) nem TECHNICAL.md (T9); o fluxo precisa funcionar end-to-end.
6. Commits literais:
   - `feat: wire LangGraph flow end to end`
   - `feat: add CLI entrypoint`
   - `chore: add sample TypeScript types`
7. Ao final: instruções de smoke test:
   ```bash
   python -m src.cli examples/types/User.ts
   ```
   e verificar arquivo em examples/mocks/.

Alinhamento SPEC: seção 7, RNF01, RNF02, RF01–RF08 (fluxo completo), §15 parcial.
```
