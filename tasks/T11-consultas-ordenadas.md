# T11 — Consultas ordenadas (2 SELECT)

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | P |
| Depende de | T03 |
| Bloqueia | T13 |
| Requisitos | RF-13, RF-14, RNF-03 |

## Objetivo
Listar todas as despesas e todos os investimentos de um usuário, **do mais recente ao mais antigo**, com ordem determinística.

## Especificação
Arquivo: `database/comandos/fintech-comandos.sql`, seção **4. CONSULTAS ORDENADAS**.

| Item | Tabela | Filtro | Ordenação (D-08) |
|---|---|---|---|
| 4.1 Despesas do usuário (RF-13) | `T_SF_GASTO` | `id_usuario = [CÓDIGO DO USUÁRIO]` | `ORDER BY dt_gasto DESC, id_gasto DESC` |
| 4.2 Investimentos do usuário (RF-14) | `T_SF_INVESTIMENTO` | `id_usuario = [CÓDIGO DO USUÁRIO]` | `ORDER BY dt_aplicacao DESC, id_investimento DESC` |

Regras:
- Mesmas colunas das consultas simples (T10), sem `SELECT *`.
- Desempate por ID é obrigatório: sem ele, dois registros na mesma data podem voltar em ordem diferente a cada execução.
- Sem paginação (fora do escopo); registrar `OFFSET … FETCH NEXT … ROWS ONLY` (12c+) como melhoria para o Java.

## Critérios de aceitação
- [ ] 2 consultas com título do enunciado
- [ ] `ORDER BY` com data `DESC` + ID `DESC`
- [ ] TC-O01 e TC-O02 aprovados em T13

## Casos de teste (executados em T13)
- TC-O01 Despesas de U1 → todas as despesas de U1 (e só dele), na ordem exata de `resultados-esperados.md`, incluindo o empate de data
- TC-O02 Investimentos de U1 → idem; investimentos de U2 → 0 linhas

## Artefatos de saída
- `database/comandos/fintech-comandos.sql` (seção 4)
