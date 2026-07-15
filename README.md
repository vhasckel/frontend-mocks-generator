# Frontend Mocks Generator

Agente inteligente baseado em **LangGraph** e **MCP** que lê models TypeScript (interfaces, types e enums) e gera automaticamente arquivos de mock compatíveis.

## Pré-requisitos

- Python **3.11+**
- Conta OpenAI e chave de API (`OPENAI_API_KEY`)
- Git (opcional, para clonar o repositório)

## Pré-requisitos

- Python **3.11+**
- Chave da API Gemini (faixa gratuita via [Google AI Studio](https://aistudio.google.com/apikey))

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
GEMINI_MODEL=gemini-2.0-flash
PROJECT_ROOT=.
MOCKS_OUTPUT_DIR=examples/mocks
MAX_FILE_SIZE_BYTES=100000
```

Nunca coloque API keys no código-fonte.

## Uso

```bash
python -m src.cli examples/types/User.ts
```
