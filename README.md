# Frontend Mocks Generator

Agente inteligente baseado em **LangGraph** e **MCP** que lê models TypeScript (interfaces, types e enums) e gera automaticamente arquivos de mock compatíveis.

## Problema

Durante o desenvolvimento frontend, a UI costuma avançar antes da API estar pronta. Criar mocks manualmente é repetitivo, sujeito a inconsistências entre desenvolvedores e fácil de ficar desalinhado do model TypeScript real.

## Objetivo

Automatizar a geração de mocks TypeScript a partir de um arquivo de model (interface, type ou enum), interpretando a estrutura com LLM e persistindo um arquivo de mock válido e padronizado.

## Fluxo com LangGraph

O agente é um grafo LangGraph com estado compartilhado (`MockAgentState`). Fluxo feliz:

```
START → read → interpret → generate → validate → write → respond → END
```

| Nó | Função |
| --- | --- |
| `read` | Lê o `.ts` de entrada |
| `interpret` | Extrai models exportados via Gemini |
| `generate` | Monta o mock com heurísticas em `src/rules/` |
| `validate` | Checa estrutura do código gerado |
| `write` | Grava o arquivo (sem sobrescrever) |
| `respond` | Monta a mensagem final de sucesso ou erro |

Em falha após `read`, `interpret`, `generate` ou `validate`, o grafo faz short-circuit direto para `respond`. Detalhes em [docs/TECHNICAL.md](docs/TECHNICAL.md).

## Ferramenta utilizada pelo agente

O agente usa uma ferramenta **MCP de filesystem** (`src/mcp/`) para:

- **ler** o model TypeScript de entrada;
- **verificar** se o mock de destino já existe;
- **escrever** o arquivo gerado.

Na v1 essa camada é uma abstração in-process (`FilesystemMCPClient`), sandboxed em `PROJECT_ROOT` — não um servidor MCP externo.

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

### Se o mock já existir

A escrita não sobrescreve (RN03). Remova o arquivo de destino ou escolha outro model antes de regenerar.

## Exemplo de entrada

Arquivo: `examples/types/User.ts`

```ts
export interface User {
  id: number;
  name: string;
  email: string;
  active: boolean;
}
```

Outro exemplo: `examples/types/AddressUser.ts`.

## Exemplo de saída

Arquivo gerado: `examples/mocks/user.mock.ts`

```ts
import { User } from '../types/User';

export const userMock: User = {
  id: 1,
  name: 'João Silva',
  email: 'user@email.com',
  active: true,
};
```

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
  prompts/        # prompts de runtime da LLM (ex.: interpret)
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
| [docs/prompts/](docs/prompts/) | Prompts de runtime da LLM (carregados pelo agente) |
| [docs/tasks/](docs/tasks/) | Etapas T0–T9, branches, critérios de aceite e prompts de implementação |

## Decisões principais

- **LangGraph** orquestra o fluxo com estado compartilhado (`MockAgentState`) e short-circuit para `respond` em falha.
- **Gemini** (`ChatGoogleGenerativeAI` + `GOOGLE_API_KEY`) interpreta o model TypeScript; a geração dos valores do mock usa heurísticas determinísticas em `src/rules/`, não Faker.
- **MCP de filesystem** na v1 é uma abstração in-process (`src/mcp/`), sandboxed em `PROJECT_ROOT`, não um servidor MCP externo.
- Escrita de mock **não sobrescreve** arquivos existentes (RN03).
- Prompts de runtime ficam em `docs/prompts/`; prompts usados para planejar/implementar o agente ficam em `docs/tasks/`.

## Limitações da solução

Factories, Faker, MSW, Storybook, Prisma, Swagger/OpenAPI e demais itens da SPEC §3 / §16 não fazem parte desta versão. A geração de valores é heurística (nome/tipo da propriedade), não um gerador estatístico de dados realistas. O MCP da v1 não é um servidor externo.
