# T10 — Consultas simples (3 SELECT)

| Campo | Valor |
|---|---|
| Status | ⬜ A fazer |
| Tamanho | P |
| Depende de | T03 |
| Bloqueia | T13 |
| Requisitos | RF-10 a RF-12, RNF-03, RNF-05 |

## Objetivo
Consultar um registro específico por código, retornando os dados relevantes para a tela correspondente.

## Especificação
Arquivo: `database/comandos/fintech-comandos.sql`, seção **3. CONSULTAS SIMPLES**.

| Item | Tabela | Colunas retornadas | Filtro |
|---|---|---|---|
| 3.1 Usuário (RF-10) | `T_SF_USUARIO` | id_usuario, nome, email, avatar, dt_cadastro, ativo | `id_usuario = [CÓDIGO DO USUÁRIO]` |
| 3.2 Despesa (RF-11) | `T_SF_GASTO` | id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante | `id_gasto = [CÓDIGO DO GASTO] AND id_usuario = [CÓDIGO DO USUÁRIO]` |
| 3.3 Investimento (RF-12) | `T_SF_INVESTIMENTO` | todas as colunas de D-01 | `id_investimento = [CÓDIGO DO INVESTIMENTO] AND id_usuario = [CÓDIGO DO USUÁRIO]` |

Regras:
- **Proibido `SELECT *`** (contrato explícito com o Java; resiste a mudanças de schema).
- **`senha` nunca é retornada** (D-05).
- Sem `JOIN` obrigatório. *Opcional*: trazer `nome` da categoria e `nm_banco` da conta via `JOIN` em 3.2 — só se não complicar; registrar a escolha.

## Critérios de aceitação
- [ ] 3 consultas com título do enunciado
- [ ] Nenhum `SELECT *`, nenhuma coluna `senha`
- [ ] Filtros com os códigos exigidos pelo enunciado
- [ ] TC-S01 a TC-S04 aprovados em T13

## Casos de teste (executados em T13)
- TC-S01 Consultar U1 → 1 linha, sem coluna senha
- TC-S02 Consultar gasto de U1 com códigos corretos → 1 linha
- TC-S03 Consultar gasto de U1 informando U2 como usuário → 0 linhas
- TC-S04 Consultar investimento de U1 → 1 linha; com ID 999 → 0 linhas

## Artefatos de saída
- `database/comandos/fintech-comandos.sql` (seção 3)
