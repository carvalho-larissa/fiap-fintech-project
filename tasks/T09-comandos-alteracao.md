# T09 — Comandos de alteração (4 UPDATE)

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | P |
| Depende de | T03 |
| Bloqueia | T13 |
| Requisitos | RF-06 a RF-09, RNF-03, RNF-05 |

## Objetivo
Escrever os 4 comandos de alteração, garantindo que cada um afete **somente** o registro correto.

## Contexto
O enunciado reforça: *"sempre use o código (ID) do que você quer alterar para garantir que o comando afete somente o registro correto"*. Para receita, despesa e investimento, o filtro deve usar **o código do usuário e o código do registro**.

## Especificação
Arquivo: `database/comandos/fintech-comandos.sql`, seção **2. ALTERAÇÃO**.

| Item | Tabela | `SET` (colunas editáveis, D-06) | `WHERE` obrigatório |
|---|---|---|---|
| 2.1 Usuário (RF-06) | `T_SF_USUARIO` | nome, email, avatar | `id_usuario = [CÓDIGO DO USUÁRIO]` |
| 2.2 Receita (RF-07) | `T_SF_RECEITA` | id_conta, id_categoria, descricao, valor, dt_recebimento, origem, recorrencia, comprovante | `id_receita = [CÓDIGO DA RECEITA] AND id_usuario = [CÓDIGO DO USUÁRIO]` |
| 2.3 Despesa (RF-08) | `T_SF_GASTO` | id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante | `id_gasto = [CÓDIGO DO GASTO] AND id_usuario = [CÓDIGO DO USUÁRIO]` |
| 2.4 Investimento (RF-09) | `T_SF_INVESTIMENTO` | id_conta, nm_investimento, tipo, instituicao, vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento, status | `id_investimento = [CÓDIGO DO INVESTIMENTO] AND id_usuario = [CÓDIGO DO USUÁRIO]` |

Regras:
- **Nunca** no `SET`: PK, `id_usuario`, `senha` (D-05), `dt_cadastro`.
- Mesmas regras de máscara de T08.
- Sem `COMMIT` (D-07).

## Critérios de aceitação
- [ ] 4 comandos, cada um com título do enunciado
- [ ] Todo `UPDATE` tem `WHERE` pela PK; 2.2–2.4 também por `id_usuario`
- [ ] Nenhuma coluna proibida no `SET`
- [ ] TC-A01 a TC-A07 aprovados em T13

## Casos de teste (executados em T13)
- TC-A01 Alterar usuário existente → `1 row updated`; demais usuários inalterados
- TC-A02 Alterar e-mail para um já usado por outro usuário → `ORA-00001`
- TC-A03 Alterar receita com usuário e receita corretos → `1 row updated`
- TC-A04 Alterar receita com **usuário errado** (receita existe, mas é de outro usuário) → `0 rows updated` ← prova do filtro duplo
- TC-A05 Alterar gasto correto → `1 row updated`
- TC-A06 Alterar gasto com usuário errado → `0 rows updated`
- TC-A07 Alterar investimento (incl. `status = 'RESGATADO'`) → `1 row updated`

## Artefatos de saída
- `database/comandos/fintech-comandos.sql` (seção 2)
