# T4 — Nós read e interpret

## Objetivo

Implementar o nó de leitura via MCP e o nó de interpretação via LLM (RF01–RF04), com primeiros mapeamentos de erro da seção 13.

## Branch

`feature/04-nodes-read-interpret`

## Depende de

`feature/03-langgraph-state` já mergeada em `main`

## Arquivos esperados

```
src/agent/nodes/read.py
src/agent/nodes/interpret.py
```

## Critérios de aceite da etapa

- [ ] `read_node` usa tools MCP (`src/mcp/tools.py`) e preenche `source_code` / `errors` / `status`
- [ ] Arquivo inexistente → mensagem `"Arquivo não encontrado."`
- [ ] Extensão inválida / não-TS → `"O arquivo informado não é um arquivo TypeScript válido."`
- [ ] `interpret_node` usa LLM (langchain-google-genai / Gemini) para extrair interfaces, types e enums exportados
- [ ] Se nada exportado for encontrado → `"Nenhuma interface exportada foi encontrada."` (ou mensagem da SPEC; manter texto exato)
- [ ] Atualiza `parsed_model` no estado
- [ ] Sem generate/validate/write/graph/CLI

## Commits sugeridos

1. `feat: add read node via MCP`
2. `feat: add LLM interpret node for TS models`

## Prompt

```
Você está implementando a etapa T4 do projeto frontend-mocks-generator.

Pré-requisito: `feature/03-langgraph-state` mergeada em `main`. Leia docs/SPEC.md (RF01–RF04, seção 5 Entrada, seção 13 erros, RN01) e use o estado em src/agent/state.py e as tools em src/mcp/tools.py.

Objetivo:
1. `git checkout main`. Crie `feature/04-nodes-read-interpret`.
2. Implemente `src/agent/nodes/read.py`:
   - Função `read_node(state: MockAgentState) -> dict` (padrão LangGraph: retorna partial state update)
   - Validar `input_path` presente; verificar existência via MCP; verificar extensão `.ts`
   - Em sucesso: setar `source_code` com o conteúdo lido
   - Em falha: popular `errors` com as mensagens EXATAS da SPEC seção 13 quando aplicável:
     - "Arquivo não encontrado."
     - "O arquivo informado não é um arquivo TypeScript válido."
   - Ajustar `status` para error quando falhar
3. Implemente `src/agent/nodes/interpret.py`:
   - Função `interpret_node(state) -> dict`
   - Se state já tem errors críticos / sem source_code, short-circuit
   - Chamar LLM (ChatGoogleGenerativeAI / langchain-google-genai; API key via env `GOOGLE_API_KEY`) com prompt estruturado pedindo JSON com:
     - name, kind (interface | type | enum), properties[{name, type, optional}], enums values, nested objects
   - Identificar interfaces, types e enums (RF04)
   - Se nenhuma estrutura exportada relevante: errors.append("Nenhuma interface exportada foi encontrada.")
   - Em sucesso: setar `parsed_model`
4. NÃO implemente generate, validate, write, respond, graph.py ou CLI.
5. Commits literais:
   - `feat: add read node via MCP`
   - `feat: add LLM interpret node for TS models`
6. Ao final: como testar os nós isoladamente (invocar com state fake / arquivo examples futuro).

Alinhamento SPEC: RF01, RF02, RF03, RF04, RN01, seção 13.
```
