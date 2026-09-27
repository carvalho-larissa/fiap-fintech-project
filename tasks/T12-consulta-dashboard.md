# T12 — Consulta do dashboard (1 SELECT)

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | G |
| Depende de | T03 |
| Bloqueia | T13 |
| Requisitos | RF-15, RNF-03 |

## Objetivo
Em **uma única linha**, retornar as principais informações do usuário + sua última despesa + seu último investimento.

## Contexto
É o item de maior risco técnico da atividade. Erros comuns que esta especificação evita:
- `JOIN` direto com as duas tabelas → **produto cartesiano** (N gastos × M investimentos linhas).
- `INNER JOIN` → usuário sem gasto ou sem investimento **some** do dashboard.
- `MAX(dt_gasto)` + join por data → retorna **2 linhas** quando há empate de data.
- `ROWNUM` antes do `ORDER BY` → pega um registro qualquer, não o mais recente.

## Especificação
Arquivo: `database/comandos/fintech-comandos.sql`, seção **5. DASHBOARD**.

Colunas (D-11), com aliases que deixam a origem clara:
`id_usuario, nome, email, dt_cadastro, id_ultimo_gasto, descricao_ultimo_gasto, valor_ultimo_gasto, dt_ultimo_gasto, tipo_ultimo_gasto, id_ultimo_investimento, nm_ultimo_investimento, tipo_ultimo_investimento, vl_ultimo_investimento, dt_ultimo_investimento`

Abordagem recomendada (compatível com 19c, D-16):
1. Subconsulta de gastos com `ROW_NUMBER() OVER (PARTITION BY id_usuario ORDER BY dt_gasto DESC, id_gasto DESC) AS rn`, filtrando `rn = 1`.
2. Idem para investimentos (`dt_aplicacao DESC, id_investimento DESC`).
3. `T_SF_USUARIO u LEFT JOIN (1) ON … LEFT JOIN (2) ON …`.
4. `WHERE u.id_usuario = [CÓDIGO DO USUÁRIO]`.
5. Aplicar o filtro de usuário **também dentro** das subconsultas (evita calcular `ROW_NUMBER` para todos os usuários — boa prática de performance).

Alternativa aceitável: `OUTER APPLY` / `LEFT JOIN LATERAL` com `FETCH FIRST 1 ROW ONLY` (12c+). Escolher uma e registrar o motivo no comentário do comando.

## Critérios de aceitação
- [ ] 1 comando com título do enunciado e comentário curto explicando a lógica
- [ ] Retorna **exatamente 1 linha** para usuário existente em todos os cenários de T07
- [ ] Retorna **0 linhas** para usuário inexistente
- [ ] Sem `SELECT *`, sem `senha`
- [ ] TC-D01 a TC-D06 aprovados em T13

## Casos de teste (executados em T13)
- TC-D01 U1 (gastos + investimentos) → 1 linha com o gasto e o investimento mais recentes
- TC-D02 U1 com empate de data → escolhe o maior ID (D-08), e continua 1 linha
- TC-D03 U2 (sem investimentos) → 1 linha, colunas de investimento nulas
- TC-D04 U3 (sem gastos) → 1 linha, colunas de gasto nulas
- TC-D05 U4 (sem movimentação) → 1 linha, só dados do usuário
- TC-D06 ID 999 → 0 linhas; e o gasto mais recente de U2 **não** aparece para U1 (isolamento)

## Artefatos de saída
- `database/comandos/fintech-comandos.sql` (seção 5)
