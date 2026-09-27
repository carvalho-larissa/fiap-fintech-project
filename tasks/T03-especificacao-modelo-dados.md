# T03 — Especificação do modelo de dados (dicionário)

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | M |
| Depende de | T02 |
| Bloqueia | T04, T06, T08–T12 |
| Requisitos | RNF-02, RNF-06, RNF-07 |

## Objetivo
Transformar o modelo físico da Fase 3 (que hoje só existe como desenho em PDF) em uma **especificação textual única e verificável**, já com as evoluções aprovadas em T02. Ela é a fonte da verdade para o DDL, o diagrama e os comandos.

## Contexto
Levantamento do `modelagem-de-dados.pdf` (modelo físico, Fase 3) — obrigatoriedade conferida pelos asteriscos do diagrama:

| Tabela | Colunas (obrigatória = ●, opcional = ○) |
|---|---|
| `T_SF_USUARIO` | ● id_usuario, ● nome(150), ● email(255), ● senha(255), ○ avatar(500), ● dt_cadastro, ● ativo CHAR(1) |
| `T_SF_CONTA_BANCARIA` | ● id_conta, ● id_usuario(FK), ● nm_banco(100), ● tipo_conta(20), ● nr_conta(20), ● ativa CHAR(1) |
| `T_SF_CATEGORIA` | ● id_categoria, ● nome(80), ● tipo(10) |
| `T_SF_RECEITA` | ● id_receita, ● id_usuario(FK), ● id_conta(FK), ● id_categoria(FK), ● descricao(300), ● valor(15,2), ● dt_recebimento, ○ origem(20), ○ recorrencia(10), ○ comprovante(500) |
| `T_SF_GASTO` | ● id_gasto, ● id_usuario(FK), ● id_conta(FK), ● id_categoria(FK), ● descricao(300), ● valor(15,2), ● dt_gasto, ○ tipo(10), ○ comprovante(500) |
| `T_SF_DIVIDA` | ● id_divida, ● id_usuario(FK), ● descricao(200), ● tipo(20), ● vl_total, ● saldo_devedor, ● total_parcelas(4), ○ tx_juros_mensal(5,4), ● status(15), ● dt_inicio |
| `T_SF_PARCELA` | ● id_parcela, ● id_divida(FK), ● nr_parcela(4), ● vl_parcela, ● dt_vencimento, ● dt_pagamento ⚠, ● status(15) |
| `T_SF_META` | ● id_meta, ● id_usuario(FK), ● nome(150), ● vl_alvo, ● vl_acumulado, ● prazo, ● status(15), ● dt_criacao |
| `T_SF_APORTE_META` | ● id_aporte, ● id_meta(FK), ● valor(15,2), ● dt_aporte, ○ observacao(300) |
| `T_SF_INVESTIMENTO` 🆕 | conforme D-01 |

⚠ = inconsistência tratada em D-15.

## Escopo
**Inclui:** as 10 tabelas (9 da Fase 3 + investimento), constraints, domínios, nomes de constraints.
**Não inclui:** índices de performance além dos implícitos (PK/UNIQUE) — ver nota.

## Especificação
Publicar `docs/05-banco-de-dados/dicionario-de-dados.md` com, para **cada tabela**: finalidade, colunas (nome, tipo Oracle, nulo, default, descrição), PK, FKs, UNIQUE e CHECKs.

**Convenção de nomes de constraints** (seguindo o padrão já presente no diagrama da Fase 3):
- PK: `PK_<TABELA>` (ex.: `PK_T_SF_GASTO`)
- FK: `FK_<TABELA>_<TABELA_REF>` (ex.: `FK_T_SF_GASTO_T_SF_USUARIO`) — nomes ≤ 128 caracteres (limite 12.2+)
- UNIQUE: `UK_<TABELA>_<COLUNA>` · CHECK: `CK_<TABELA>_<COLUNA>`

**Domínios (D-04)**:

| Coluna | Valores permitidos |
|---|---|
| `T_SF_USUARIO.ativo`, `T_SF_CONTA_BANCARIA.ativa` | `S`, `N` (default `S`) |
| `T_SF_CONTA_BANCARIA.tipo_conta` | `CORRENTE`, `POUPANCA`, `PAGAMENTO`, `SALARIO`, `INVESTIMENTO` |
| `T_SF_CATEGORIA.tipo` | `RECEITA`, `GASTO` |
| `T_SF_RECEITA.origem` | `SALARIO`, `FREELANCE`, `INVESTIMENTO`, `OUTROS` |
| `T_SF_RECEITA.recorrencia` | `UNICA`, `MENSAL`, `ANUAL` |
| `T_SF_GASTO.tipo` | `FIXO`, `VARIAVEL` |
| `T_SF_DIVIDA.status` | `EM_DIA`, `ATRASADA`, `QUITADA` |
| `T_SF_PARCELA.status` | `PENDENTE`, `PAGA`, `ATRASADA` |
| `T_SF_META.status` | `ATIVA`, `CONCLUIDA`, `CANCELADA` |
| `T_SF_INVESTIMENTO.tipo` / `.status` | conforme D-01 |

**Regras numéricas**: todo `valor`/`vl_*` monetário `> 0` (exceto `saldo_devedor` e `vl_acumulado`: `>= 0`); `total_parcelas`/`nr_parcela` `> 0`; taxas (`tx_*`) como fração decimal `>= 0` (D-17).

**Integridade conta × usuário (D-14)**: `UK_T_SF_CONTA_BANCARIA_CONTA_USUARIO UNIQUE (id_conta, id_usuario)` em `T_SF_CONTA_BANCARIA`; em `T_SF_RECEITA`, `T_SF_GASTO` e `T_SF_INVESTIMENTO` a FK para conta é **composta** `(id_conta, id_usuario)` (a FK simples para `T_SF_USUARIO` é mantida).

**Parcela (D-15)**: `dt_pagamento` anulável; `CHECK (status <> 'PAGA' OR dt_pagamento IS NOT NULL)`.

**Colunas usadas pelos comandos desta atividade** (marcar no dicionário para rastreabilidade):
`T_SF_USUARIO`, `T_SF_CONTA_BANCARIA`, `T_SF_RECEITA`, `T_SF_GASTO`, `T_SF_INVESTIMENTO` (+ `T_SF_CATEGORIA` como pré-requisito de FK).

## Critérios de aceitação
- [ ] Dicionário cobre as 10 tabelas, sem coluna do PDF faltando ou renomeada sem registro
- [ ] Toda diferença em relação à Fase 3 listada numa seção "Evoluções em relação à Fase 3" com a decisão que a justifica (D-xx)
- [ ] Todos os domínios `CHECK` definidos e cabem no tamanho da coluna (ex.: `VARIAVEL` ≤ 10)
- [ ] Nomes de constraints seguem a convenção e são únicos
- [ ] Revisado pela responsável

## Artefatos de saída
- `docs/05-banco-de-dados/dicionario-de-dados.md`

## Riscos e notas
- Índices em FKs (`id_usuario` nas tabelas filhas) melhoram as consultas ordenadas e o dashboard; registrar como recomendação e criar no DDL (baixo custo, sem impacto no entregável).
- Os tamanhos de `VARCHAR2` seguem a Fase 3; não aumentar sem motivo registrado.
