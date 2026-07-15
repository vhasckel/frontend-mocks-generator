# Frontend Mocks Generator

Agente inteligente baseado em **LangGraph** e **MCP** que lê models TypeScript (interfaces, types e enums) e gera automaticamente arquivos de mock compatíveis.

## Pré-requisitos

- Python **3.11+**
- Chave da API Gemini (faixa gratuita via [Google AI Studio](https://aistudio.google.com/apikey))
- Git (opcional, para clonar o repositório)

## Setup

```bash
git clone git@github.com:vhasckel/frontend-mocks-generator.git
cd frontend-mocks-generator

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
# ou: pip install -e .

cp .env.example .env
```

Edite `.env` e preencha:

```bash
GOOGLE_API_KEY=...
GEMINI_MODEL=gemini-3.1-flash-lite
PROJECT_ROOT=.
MOCKS_OUTPUT_DIR=examples/mocks
MAX_FILE_SIZE_BYTES=100000
```

Nunca coloque API keys no código-fonte.

`GEMINI_MODEL` é opcional; o default do código é `gemini-2.0-flash`. Contas novas podem precisar de um modelo ainda disponível na faixa gratuita (ex.: `gemini-3.1-flash-lite` ou `gemini-3-flash-preview`).

## Uso

Com o venv ativo e `.env` configurado:

```bash
python -m src.cli examples/types/User.ts
```

Em sucesso, a CLI imprime o caminho do mock (por padrão em `examples/mocks/`, ex.: `examples/mocks/user.mock.ts`) e retorna exit code `0`. Em falha, imprime a mensagem de erro da SPEC §13 e retorna `!= 0`.

Outros exemplos de entrada: `examples/types/AddressUser.ts`.

### Se o mock já existir

A escrita não sobrescreve (RN03). Remova o arquivo de destino ou escolha outro model antes de regenerar.

## Estrutura de pastas

```
src/
  agent/          # grafo LangGraph, estado, LLM (Gemini) e nós do fluxo
  mcp/            # cliente e tools de filesystem (MCP)
  rules/          # heurísticas de geração de valores
  security/       # validação de path, tamanho e mensagens de erro
  cli.py          # ponto de entrada: python -m src.cli
examples/
  types/          # models TypeScript de exemplo
  mocks/          # mocks gerados
docs/
  SPEC.md         # especificação do produto
  TECHNICAL.md    # arquitetura e detalhes de implementação
  tasks/          # fluxo de implementação por etapas (T0–T9)
.env.example
pyproject.toml
requirements.txt
```

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [docs/SPEC.md](docs/SPEC.md) | Requisitos, regras de negócio, critérios de aceite, evoluções |
| [docs/TECHNICAL.md](docs/TECHNICAL.md) | Arquitetura, módulos, estado, variáveis de ambiente, limitações da v1 |
| [docs/tasks/](docs/tasks/) | Etapas T0–T9, branches, critérios de aceite e prompts |

## Fora do escopo (v1)

Factories, Faker, MSW, Storybook, Prisma, Swagger/OpenAPI e demais itens da SPEC §3 / §16 não fazem parte desta versão.
