# Agente Gerador de Mocks para Frontend

# 1. Visão Geral

## 1.1 Objetivo

O objetivo deste projeto é desenvolver um agente inteligente capaz de automatizar a geração de arquivos de mock para aplicações frontend a partir de modelos TypeScript.

O agente deverá receber como entrada um arquivo contendo uma interface, type ou enum, interpretar sua estrutura utilizando um Modelo de Linguagem (LLM) e gerar automaticamente um arquivo de mock compatível com o modelo informado.

O agente será implementado utilizando **LangGraph** para orquestração do fluxo, **MCP (Model Context Protocol)** para interação com o sistema de arquivos e uma LLM para interpretação e geração do código.

---

## 1.2 Problema

Durante o desenvolvimento de aplicações frontend é comum que a interface gráfica seja implementada antes da conclusão da API.

Nesse cenário, desenvolvedores precisam criar manualmente arquivos de mock para simular os dados retornados pelo backend.

Esse processo apresenta diversos problemas:

- criação repetitiva de estruturas semelhantes;
- perda de tempo em tarefas pouco produtivas;
- inconsistência entre mocks criados por diferentes desenvolvedores;
- dificuldade de manutenção;
- possibilidade de incompatibilidade entre o mock e o modelo real.

O agente proposto automatiza essa atividade, reduzindo tempo de desenvolvimento e aumentando a padronização do projeto.

---

# 2. Objetivos

## 2.1 Objetivo Geral

Automatizar a geração de mocks TypeScript para aplicações frontend.

---

## 2.2 Objetivos Específicos

O agente deverá ser capaz de:

- ler arquivos TypeScript;
- interpretar interfaces;
- interpretar tipos (type);
- interpretar enums;
- compreender propriedades e seus tipos;
- gerar valores coerentes para cada propriedade;
- criar automaticamente arquivos de mock;
- validar o código gerado;
- retornar mensagens claras ao usuário.

---

# 3. Escopo

## Incluído

Faz parte do escopo:

- leitura de arquivos `.ts`;
- leitura de interfaces TypeScript;
- leitura de tipos (`type`);
- leitura de enums;
- geração de mocks;
- escrita dos arquivos gerados;
- utilização de LangGraph;
- utilização de ferramentas via MCP;
- utilização de memória através do estado do LangGraph.

---

## Fora do Escopo

Não faz parte desta primeira versão:

- geração de testes automatizados;
- integração com bancos de dados;
- geração de documentação;
- suporte a Swagger/OpenAPI;
- suporte ao Prisma;
- geração automática de APIs;
- execução automática de testes.

Essas funcionalidades poderão ser implementadas em versões futuras.

---

# 4. Público-alvo

O agente é destinado principalmente a:

- desenvolvedores frontend;
- desenvolvedores full stack;
- estudantes;
- equipes que utilizam React, Angular, Vue ou aplicações TypeScript.

---

# 5. Entrada

A entrada do agente consiste em um caminho para um arquivo TypeScript.

Exemplo:

```
src/types/User.ts
```

Conteúdo:

```ts
export interface User {
  id: number;
  name: string;
  email: string;
  active: boolean;
}
```

---

# 6. Saída

O agente deverá produzir automaticamente um arquivo de mock.

Exemplo:

```
src/mocks/user.mock.ts
```

Conteúdo:

```ts
import { User } from '../types/User';

export const userMock: User = {
  id: 1,
  name: 'João Silva',
  email: 'joao@email.com',
  active: true,
};
```

---

# 7. Fluxo Geral

```
Usuário

↓

Seleciona arquivo

↓

Leitura via MCP

↓

Interpretação pelo LLM

↓

Geração do mock

↓

Validação

↓

Escrita do arquivo

↓

Resposta ao usuário
```

---

# 8. Requisitos Funcionais

## RF01

O agente deverá receber um arquivo TypeScript como entrada.

---

## RF02

O agente deverá utilizar uma ferramenta MCP para realizar a leitura do arquivo.

---

## RF03

O agente deverá interpretar a estrutura do arquivo utilizando uma LLM.

---

## RF04

O agente deverá identificar interfaces, types e enums presentes no arquivo.

---

## RF05

O agente deverá gerar valores coerentes para cada propriedade encontrada.

---

## RF06

O agente deverá gerar um arquivo TypeScript válido.

---

## RF07

O agente deverá utilizar uma ferramenta MCP para gravar o arquivo gerado.

---

## RF08

O agente deverá informar ao usuário o resultado da operação.

---

# 9. Requisitos Não Funcionais

## RNF01

O agente deverá ser implementado utilizando LangGraph.

---

## RNF02

O agente deverá utilizar memória através do estado compartilhado.

---

## RNF03

O agente deverá utilizar pelo menos uma ferramenta MCP.

---

## RNF04

O código deverá ser organizado em módulos.

---

## RNF05

O agente deverá possuir documentação técnica.

---

## RNF06

O projeto deverá estar versionado no GitHub.

---

# 10. Regras de Negócio

## RN01

Somente arquivos `.ts` poderão ser processados.

---

## RN02

O agente deverá impedir escrita fora do diretório configurado.

---

## RN03

Caso o mock já exista, o agente deverá informar o usuário.

---

## RN04

O agente deverá gerar apenas propriedades existentes no modelo.

---

## RN05

Nenhuma propriedade poderá ser inventada.

---

## RN06

Os tipos deverão ser respeitados.

---

# 11. Regras de Geração

## String

Exemplo

```ts
name: 'João Silva';
```

---

## Number

```ts
price: 199.9;
```

---

## Boolean

```ts
active: true;
```

---

## Date

```ts
createdAt: new Date().toISOString();
```

---

## Email

```ts
email: 'user@email.com';
```

---

## Telefone

```ts
phone: '(11) 99999-9999';
```

---

## CPF

```ts
cpf: '123.456.789-09';
```

---

## CNPJ

```ts
cnpj: '12.345.678/0001-90';
```

---

## UUID

```ts
id: '550e8400-e29b-41d4-a716-446655440000';
```

---

## Arrays

O agente deverá gerar entre 2 e 5 elementos.

Exemplo

```ts
roles: ['ADMIN', 'USER'];
```

---

## Objetos

Objetos deverão ser gerados recursivamente.

---

## Enums

O primeiro valor disponível deverá ser utilizado como padrão.

---

# 12. Segurança

O agente deverá implementar validações básicas.

## Validação da entrada

- verificar se o arquivo existe;
- verificar extensão;
- limitar tamanho do arquivo.

---

## Escrita

- impedir escrita fora do projeto;
- impedir sobrescrita sem confirmação.

---

## API Keys

As credenciais deverão permanecer armazenadas em variáveis de ambiente.

Nunca deverão ser armazenadas diretamente no código-fonte.

---

# 13. Tratamento de Erros

O agente deverá tratar os seguintes cenários:

## Arquivo inexistente

Mensagem:

```
Arquivo não encontrado.
```

---

## Arquivo inválido

Mensagem:

```
O arquivo informado não é um arquivo TypeScript válido.
```

---

## Interface não encontrada

Mensagem:

```
Nenhuma interface exportada foi encontrada.
```

---

## Falha na escrita

Mensagem:

```
Não foi possível criar o arquivo de mock.
```

---

## Erro inesperado

Mensagem:

```
Erro interno durante a geração do mock.
```

---

# 14. Casos de Uso

## Caso 1

### Gerar mock simples

Entrada

```ts
interface User {
  id: number;
  name: string;
}
```

Saída

```ts
export const userMock = {
  id: 1,
  name: 'João Silva',
};
```

---

## Caso 2

### Interface com objeto interno

Entrada

```ts
interface Address {
  city: string;
}

interface User {
  address: Address;
}
```

Saída

```ts
address: {
  city: 'São Paulo';
}
```

---

## Caso 3

### Interface com array

Entrada

```ts
roles: string[]
```

Saída

```ts
roles: ['ADMIN', 'USER'];
```

---

# 15. Critérios de Aceite

O projeto será considerado concluído quando:

- [x] o agente executar o fluxo completo utilizando LangGraph;
- [x] a leitura do arquivo ocorrer via MCP;
- [x] o mock for gerado corretamente;
- [x] o arquivo for salvo automaticamente;
- [x] o estado for compartilhado entre os nós;
- [x] os erros forem tratados;
- [x] a documentação estiver completa;
- [ ] o projeto estiver publicado no GitHub.

**Status (T9):** os sete primeiros itens estão atendidos no código e na documentação após T0–T8 + T9. A leitura “via MCP” na v1 usa a abstração in-process `FilesystemMCPClient` / `mcp.tools` (não um servidor MCP externo). O item GitHub permanece aberto: o remote `origin` já aponta para `vhasckel/frontend-mocks-generator`, mas o push definitivo de `main` (incluir T8+T9) é passo residual humano. Detalhes em [TECHNICAL.md](TECHNICAL.md) §7.

---

# 16. Possíveis Evoluções

Entre as melhorias previstas para versões futuras estão:

- geração de factories;
- integração com Faker;
- geração de mocks para Storybook;
- geração de mocks para MSW;
- suporte ao Prisma;
- suporte ao Zod;
- suporte ao Swagger/OpenAPI;
- geração de fixtures para Cypress;
- geração de dados realistas utilizando IA;
- personalização das regras de geração.

---

# 17. Tecnologias Utilizadas

| Tecnologia | Finalidade                                     |
| ---------- | ---------------------------------------------- |
| Python     | Linguagem principal                            |
| LangGraph  | Orquestração do agente                         |
| LangChain  | Integração com LLM                             |
| MCP        | Ferramentas para acesso ao sistema de arquivos |
| Gemini API | Interpretação dos models TypeScript (LLM)      |
| Git        | Versionamento                                  |
| GitHub     | Hospedagem do projeto                          |

---

# 18. Resultado Esperado

Ao final da execução, o agente deverá ser capaz de receber um modelo TypeScript e produzir automaticamente um arquivo de mock válido, estruturado e compatível com o padrão do projeto, reduzindo significativamente o tempo gasto na criação manual de dados fictícios para desenvolvimento frontend.
