# T8 — Segurança e tratamento de erros

## Objetivo

Endurecer validações de entrada/escrita e garantir mensagens exatas da seção 13 (seção 12 Segurança).

## Branch

`feature/08-security-errors`

## Depende de

`feature/07-graph-cli` já mergeada em `main`

## Arquivos esperados

```
src/security/validation.py
```

(Atualizações pontuais em nodes/mcp se necessário para usar o módulo.)

## Critérios de aceite da etapa

- [ ] Validação de existência, extensão `.ts` e limite de tamanho (`MAX_FILE_SIZE_BYTES`)
- [ ] Escrita limitada ao projeto; sem sobrescrita sem confirmação/overwrite explícito
- [ ] Mensagens EXATAS:
  - `Arquivo não encontrado.`
  - `O arquivo informado não é um arquivo TypeScript válido.`
  - `Nenhuma interface exportada foi encontrada.`
  - `Não foi possível criar o arquivo de mock.`
  - `Erro interno durante a geração do mock.`
- [ ] API key ausente tratada de forma segura (mensagem clara; sem vazar secrets)

## Commits sugeridos

1. `feat: harden input validation and error messages`
2. `fix: map failure paths to SPEC error texts`

## Prompt

```
Você está implementando a etapa T8 do projeto frontend-mocks-generator.

Pré-requisito: `feature/07-graph-cli` mergeada em `main`. Leia docs/SPEC.md seções 12 e 13 por completo.

Objetivo:
1. `git checkout main`. Crie `feature/08-security-errors`.
2. Implemente `src/security/validation.py` com funções reutilizáveis:
   - validate_input_path(path) → checa extensão .ts, normaliza path, existência
   - validate_file_size(path ou content length) vs MAX_FILE_SIZE_BYTES
   - assert_within_project_root(path)
   - Constantes/mensagens centralizadas das strings EXATAS da seção 13
3. Integre essas validações nos pontos certos (read_node, mcp tools, write_node, CLI) SEM duplicar inconsistente as strings de erro.
4. Garantir short-circuit do grafo para respond com "Erro interno durante a geração do mock." em exceções não previstas (try/except no run_agent ou nó final).
5. Se GOOGLE_API_KEY ausente: falha clara antes/durante interpret, sem imprimir a key.
6. Commits literais:
   - `feat: harden input validation and error messages`
   - `fix: map failure paths to SPEC error texts`
7. Ao final: tabela rápida cenário → mensagem esperada e como reproduzir cada um manualmente.

Alinhamento SPEC: seção 12, seção 13, RN01–RN03.
```
