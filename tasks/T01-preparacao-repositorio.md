# T01 — Preparação do repositório

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | P |
| Depende de | — |
| Bloqueia | T02, T05 |
| Requisitos | — (infraestrutura) |

## Objetivo
Deixar o repositório pronto para receber os artefatos de banco de dados, com o enunciado versionado e uma branch isolada para a execução.

## Contexto
- O enunciado estava solto na raiz como `orientacoes-atividadetxt.txt` (fora do git).
- Fluxo acordado: toda mudança entra via branch + PR (nada direto em `main`).
- O plano de tarefas está sendo entregue na branch `docs/plano-tarefas-sql`.

## Especificação
1. ✅ Enunciado movido para `docs/05-banco-de-dados/orientacoes-atividade.txt` (nome normalizado).
2. ✅ Fonte editável do diagrama extraída do PDF da Fase 3 → `docs/03-modelagem-de-dados/modelo-relacional.drawio` (insumo de T04).
3. Mergear o PR do plano e criar a branch `feat/sql-comandos` a partir do `main` atualizado.
4. Criar a estrutura (pastas vazias com `.gitkeep`):
   ```
   database/ddl/
   database/dml/
   database/comandos/
   database/testes/evidencias/
   docs/05-banco-de-dados/entrega/
   ```
5. `.gitignore`: adicionar `database/.env.local` e `*.credentials` — **senhas de banco nunca são versionadas**.

## Critérios de aceitação
- [x] Enunciado versionado em `docs/05-banco-de-dados/orientacoes-atividade.txt`
- [x] `.drawio` da Fase 3 extraído e versionado
- [x] Pasta `tasks/` com plano, template e uma especificação por tarefa
- [ ] PR do plano mergeado; branch `feat/sql-comandos` criada a partir de `main`
- [ ] Estrutura `database/` criada
- [ ] `.gitignore` cobre arquivos de credencial

## Artefatos de saída
- `docs/05-banco-de-dados/orientacoes-atividade.txt`
- `docs/03-modelagem-de-dados/modelo-relacional.drawio`
- `database/**` (estrutura) · `.gitignore` (atualizado)

## Riscos e notas
- O repositório fica no OneDrive: evitar editar os mesmos arquivos em duas máquinas ao mesmo tempo (conflitos de sincronização fora do git).
