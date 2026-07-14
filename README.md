# Frontend Mocks Generator

Agente inteligente baseado em **LangGraph** e **MCP** que lê models TypeScript (interfaces, types e enums) e gera automaticamente arquivos de mock compatíveis.

A especificação completa do produto está em [`docs/SPEC.md`](docs/SPEC.md). O fluxo de implementação por etapas (branches, critérios de aceite e prompts) está em [`docs/tasks/`](docs/tasks/).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# ou: pip install -e .
cp .env.example .env
```

Preencha `OPENAI_API_KEY` em `.env` (nunca coloque API keys no código).
