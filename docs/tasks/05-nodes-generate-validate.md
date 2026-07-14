# T5 — Nós generate e validate

## Objetivo

Gerar o código do mock com as regras de negócio (seção 11, RN04–RN06) e validar o resultado (RF05, RF06).

## Branch

`feature/05-nodes-generate-validate`

## Depende de

`feature/04-nodes-read-interpret` já mergeada em `main`

## Arquivos esperados

```
src/rules/generation.py
src/agent/nodes/generate.py
src/agent/nodes/validate.py
```

## Critérios de aceite da etapa

- [ ] Regras documentadas/implementadas para: string, number, boolean, date/ISO, email, telefone, CPF, CNPJ, UUID, arrays (2–5 itens), objetos recursivos, enums (primeiro valor)
- [ ] Mock não inventa propriedades (RN04, RN05) e respeita tipos (RN06)
- [ ] `generate_node` preenche `generated_mock` e sugere `output_path` (ex.: `examples/mocks/<name>.mock.ts`)
- [ ] `validate_node` rejeita mock vazio/inválido ou com props extras vs `parsed_model`
- [ ] Sem write/respond/graph/CLI

## Commits sugeridos

1. `feat: add mock generation node with business rules`
2. `feat: add generated mock validation node`

## Prompt

```
Você está implementando a etapa T5 do projeto frontend-mocks-generator.

Pré-requisito: `feature/04-nodes-read-interpret` mergeada em `main`. Leia docs/SPEC.md (RF05, RF06, RN04–RN06, seção 6 Saída, seção 11 Regras de Geração, casos de uso seção 14).

Objetivo:
1. `git checkout main`. Crie `feature/05-nodes-generate-validate`.
2. Implemente `src/rules/generation.py` com helpers/heurísticas alinhadas à seção 11:
   - string → ex. 'João Silva' (ou valor coerente ao nome da prop)
   - number → ex. 199.9 / 1
   - boolean → true/false
   - Date / createdAt → new Date().toISOString() no código gerado
   - email → 'user@email.com'
   - phone → '(11) 99999-9999'
   - cpf / cnpj / uuid conforme exemplos da SPEC
   - arrays → entre 2 e 5 elementos
   - objetos → geração recursiva
   - enums → primeiro valor disponível
   Heurística por nome de propriedade (email, phone, cpf, etc.) é desejável.
3. Implemente `src/agent/nodes/generate.py` (`generate_node`):
   - Usa `parsed_model` + rules (+ LLM se necessário para compor o arquivo final TypeScript)
   - Saída no estilo da SPEC seção 6:
     import { User } from '...';
     export const userMock: User = { ... };
   - Preencher `generated_mock` e `output_path` (sob MOCKS_OUTPUT_DIR; nome `<entity>.mock.ts` em camelCase/arquivo consistente)
   - Nunca adicionar propriedades que não existam no modelo (RN04/RN05)
4. Implemente `src/agent/nodes/validate.py` (`validate_node`):
   - Verifica que generated_mock não está vazio
   - Verifica presença das propriedades do modelo (e ausência de extras, quando possible via parsed_model)
   - Em falha estrutural, setar errors (mensagem genérica ou específica; mensagens padrão de I/O ficam para write)
5. NÃO implemente write, respond, graph ou CLI.
6. Commits literais:
   - `feat: add mock generation node with business rules`
   - `feat: add generated mock validation node`
7. Ao final: exemplo de generated_mock esperado para interface User { id, name, email, active }.

Alinhamento SPEC: RF05, RF06, RN04, RN05, RN06, seção 11, seção 14.
```
