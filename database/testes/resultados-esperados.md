# Resultados esperados (oráculo de testes)

Escrito **antes** da execução (T07), a partir de `database/dml/02-seed.sql`. Em T13, cada consulta
executada é comparada com estas tabelas; qualquer diferença é falha.

Base: carga limpa (`00` → `01` → `02`), sem comandos de alteração aplicados.

## Massa carregada (resumo)

| Usuário | Contas | Gastos (id · data) | Investimentos (id · data) |
|---|---|---|---|
| 1 Larissa | 1 Itaú, 2 Nubank | 1 · 05/10 · 2 · 01/10 · **3 · 09/10** · **4 · 09/10** | 1 · 01/08 · **2 · 15/09** · **3 · 15/09** |
| 2 Bruno | 3 Bradesco | 5 · 10/10 · 6 · **20/10** (mais recente do banco) | — |
| 3 Carla | 4 Inter | — | 4 · 10/10 · 5 · **25/10** (mais recente do banco) |
| 4 Diego | 5 Caixa | — | — |

Datas em 2025. Em negrito: empates de data (desempate D-08) e registros usados para provar isolamento entre usuários.

## 3. Consultas simples

| Caso | Parâmetros | Esperado |
|---|---|---|
| TC-S01 | usuário 1 | 1 linha: `1, Larissa Gomes de Carvalho, larissa@exemplo.com, NULL, 01/03/2025, S`; **sem** coluna `senha` |
| TC-S02 | gasto 4, usuário 1 | 1 linha: `4, 1, 1, 4, Mercado extra, 412.30, 09/10/2025, VARIAVEL, NULL` |
| TC-S03 | gasto 4, usuário 2 | **0 linhas** (gasto existe, mas é de outro usuário) |
| TC-S04a | investimento 2, usuário 1 | 1 linha: `2, 1, 2, Tesouro Selic 2029, TESOURO, Tesouro Nacional, 1500.00, 0.1075, 15/09/2025, 01/03/2029, ATIVO` |
| TC-S04b | investimento 999, usuário 1 | **0 linhas** |

## 4. Consultas ordenadas

| Caso | Parâmetros | Ordem esperada dos IDs |
|---|---|---|
| TC-O01a | despesas do usuário 1 | **4, 3, 1, 2** (4 e 3 empatam em 09/10 → maior ID primeiro) |
| TC-O01b | despesas do usuário 2 | 6, 5 |
| TC-O01c | despesas do usuário 3 | 0 linhas |
| TC-O02a | investimentos do usuário 1 | **3, 2, 1** (3 e 2 empatam em 15/09 → maior ID primeiro) |
| TC-O02b | investimentos do usuário 3 | 5, 4 |
| TC-O02c | investimentos do usuário 2 | 0 linhas |

## 5. Dashboard

Sempre **exatamente 1 linha** para usuário existente; 0 para inexistente.

| Caso | Usuário | Último gasto (id · descrição · valor · data · tipo) | Último investimento (id · nome · tipo · valor · data) |
|---|---|---|---|
| TC-D01/D02 | 1 | 4 · Mercado extra · 412.30 · 09/10/2025 · VARIAVEL | 3 · FII HGLG11 · FII · 800.00 · 15/09/2025 |
| TC-D03 | 2 | 6 · Cinema · 60.00 · 20/10/2025 · VARIAVEL | *todas nulas* |
| TC-D04 | 3 | *todas nulas* | 5 · Ações ITUB4 · ACOES · 1000.00 · 25/10/2025 |
| TC-D05 | 4 | *todas nulas* | *todas nulas* |
| TC-D06 | 999 | **0 linhas** | |

Prova de isolamento (TC-D06): para o usuário 1 o último gasto **não** é o id 6 (20/10, do usuário 2) e o último investimento **não** é o id 5 (25/10, do usuário 3).

## 1. Cadastro (executados sobre a carga limpa, cada um revertido após o teste)

| Caso | Ação | Esperado |
|---|---|---|
| TC-C01 | novo usuário válido | 1 linha; `id_usuario = 5` (identity após o maior ID), `dt_cadastro = TRUNC(SYSDATE)`, `ativo = 'S'` |
| TC-C02 | novo usuário com `larissa@exemplo.com` | `ORA-00001` (`UK_SF_USUARIO_EMAIL`) |
| TC-C03 | conta para usuário 4 | 1 linha, `id_conta = 6` |
| TC-C04 | conta para usuário 999 | `ORA-02291` (`FK_SF_CONTA_USUARIO`) |
| TC-C05 | receita do usuário 1, conta 1, categoria 2 | 1 linha, `id_receita = 3` |
| TC-C06 | gasto do usuário 1, conta 1, categoria 6 | 1 linha, `id_gasto = 7` |
| TC-C07 | gasto com `tipo = 'fixo'` (minúsculo) | `ORA-02290` (`CK_SF_GASTO_TIPO`) |
| TC-C07b | gasto do usuário 1 na conta 3 (do usuário 2) | `ORA-02291` (`FK_SF_GASTO_CONTA` — D-14) |
| TC-C08 | investimento do usuário 4, conta 5, sem vencimento | 1 linha, `id_investimento = 6`, `status = 'ATIVO'` |

## 2. Alteração (cada um revertido após o teste)

| Caso | Ação | Esperado |
|---|---|---|
| TC-A01 | alterar usuário 4 | `1 row updated`; usuários 1–3 inalterados; `senha` e `dt_cadastro` inalterados |
| TC-A02 | alterar e-mail do usuário 4 para `bruno@exemplo.com` | `ORA-00001` |
| TC-A03 | alterar receita 2 do usuário 1 | `1 row updated` |
| TC-A04 | alterar receita 2 informando usuário 2 | **`0 rows updated`** (filtro duplo) |
| TC-A05 | alterar gasto 3 do usuário 1 | `1 row updated`; os demais gastos inalterados |
| TC-A06 | alterar gasto 3 informando usuário 2 | **`0 rows updated`** |
| TC-A07 | alterar investimento 1 do usuário 1 para `status = 'RESGATADO'` | `1 row updated` |
