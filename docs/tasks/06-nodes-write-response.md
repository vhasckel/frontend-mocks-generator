# T6 — Nós write e respond

## Objetivo

Persistir o mock via MCP e montar a resposta ao usuário (RF07, RF08, RN03).

## Branch

`feature/06-nodes-write-response`

## Depende de

`feature/05-nodes-generate-validate` já mergeada em `main`

## Arquivos esperados

```
src/agent/nodes/write.py
src/agent/nodes/respond.py
```

## Critérios de aceite da etapa

- [ ] `write_node` grava via `src/mcp/tools.py`
- [ ] Falha de escrita → `"Não foi possível criar o arquivo de mock."`
- [ ] Arquivo existente sem overwrite → warning/erro informando o usuário (RN03), sem sobrescrever silenciosamente
- [ ] `respond_node` produz mensagem final clara de sucesso ou agrega `errors` (RF08)
- [ ] Sem montar o grafo completo ou CLI (T7)

## Commits sugeridos

1. `feat: add write node via MCP`
2. `feat: add user-facing response node`

## Prompt

```
Você está implementando a etapa T6 do projeto frontend-mocks-generator.

Pré-requisito: `feature/05-nodes-generate-validate` mergeada em `main`. Leia docs/SPEC.md (RF07, RF08, RN03, seção 12 Escrita, seção 13 Falha na escrita).

Objetivo:
1. `git checkout main`. Crie `feature/06-nodes-write-response`.
2. Implemente `src/agent/nodes/write.py` (`write_node`):
   - Se validation falhou / status error / sem generated_mock: short-circuit
   - Chamar write_file MCP com output_path e content=generated_mock, overwrite=False por padrão
   - Se destino já existe: adicionar warning ou error informando o usuário (não sobrescrever silenciosamente) — alinhado a RN03
   - Se escrita falhar por permissão/IO: errors.append("Não foi possível criar o arquivo de mock.")
3. Implemente `src/agent/nodes/respond.py` (`respond_node`):
   - Montar campo de resposta no estado — se necessário, estender MockAgentState com `message: str` em src/agent/state.py (commit junto se precisar de ajuste mínimo)
   - Sucesso: informar caminho do mock criado
   - Erro: juntar errors em mensagem clara; em erro inesperado não mapeado usar "Erro interno durante a geração do mock." quando fizer sentido
4. NÃO monte graph.py completo nem CLI (deixe para T7).
5. Commits literais:
   - `feat: add write node via MCP`
   - `feat: add user-facing response node`
6. Ao final: fluxo mental read→…→write→respond e exemplos de mensagens de sucesso/erro.

Alinhamento SPEC: RF07, RF08, RN03, seções 12 e 13.
```
