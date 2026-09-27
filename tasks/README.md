# Plano de Tarefas — Atividade Fintech (Fase 4): Comandos SQL em Oracle

> **Documento-mestre.** Use como painel de controle durante a execução: atualize a coluna
> *Status* (seção 5) e marque o checklist (seção 8) ao fim de cada fase.
> Cada tarefa tem sua especificação completa no arquivo `Txx-*.md` correspondente.

| Item | Valor |
|---|---|
| Enunciado | [`docs/05-banco-de-dados/orientacoes-atividade.txt`](../docs/05-banco-de-dados/orientacoes-atividade.txt) |
| Modelo base (Fase 3) | [`docs/03-modelagem-de-dados/modelagem-de-dados.pdf`](../docs/03-modelagem-de-dados/modelagem-de-dados.pdf) · fonte editável: [`modelo-relacional.drawio`](../docs/03-modelagem-de-dados/modelo-relacional.drawio) |
| SGBD | Oracle — validação local em Docker/WSL2 (D-09); sintaxe compatível com 19c (D-16) |
| Entrega | **PDF** gerado a partir de documento Word com modelo relacional + comandos SQL (D-10) |
| Branch de execução | `feat/sql-comandos` |
| Responsável | Larissa Gomes de Carvalho — RM 571266 — 1TDSOA |

---

## 1. Objetivo

Entregar, em **um PDF**, o **modelo relacional** do sistema Fintech e os **15 comandos SQL (Oracle) com
máscaras de substituição** que a aplicação Java usará na próxima fase — todos específicos para as
tabelas do projeto e **validados em um Oracle real** antes da entrega.

## 2. Escopo

**Dentro**
- 15 comandos: 5 `INSERT`, 4 `UPDATE`, 3 consultas simples, 2 consultas ordenadas, 1 consulta de dashboard.
- Evolução do modelo: `T_SF_INVESTIMENTO` (conceito exigido e inexistente na Fase 3) + ajustes aprovados.
- Diagrama relacional atualizado (exigido na entrega).
- Artefatos de validação: DDL, massa de dados, testes, evidências.
- Documento Word → PDF; atualização da documentação do repositório.

**Fora (explicitamente)**
- `DELETE`, procedures, functions, triggers, views.
- Comandos para dívidas, parcelas, metas e aportes (as tabelas existem no DDL só para manter o modelo íntegro).
- Implementação Java/JDBC e front-end (próxima fase).
- Troca de senha (fluxo próprio — D-05).

## 3. Catálogo de requisitos

### Funcionais (item do entregável)

| ID | Requisito (enunciado) | SQL | Tarefa |
|---|---|---|---|
| RF-01 | Cadastrar os dados de um novo usuário | INSERT | T08 |
| RF-02 | Cadastrar os dados da conta bancária de um usuário | INSERT | T08 |
| RF-03 | Cadastrar os dados de uma nova receita para um usuário | INSERT | T08 |
| RF-04 | Cadastrar os dados de uma nova despesa (gasto) de um usuário | INSERT | T08 |
| RF-05 | Cadastrar os dados de um novo investimento feito por um usuário | INSERT | T08 |
| RF-06 | Alterar os dados de um usuário (pelo código do usuário) | UPDATE | T09 |
| RF-07 | Alterar uma receita (código do usuário + código da receita) | UPDATE | T09 |
| RF-08 | Alterar uma despesa (código do usuário + código da despesa) | UPDATE | T09 |
| RF-09 | Alterar um investimento (código do usuário + código do investimento) | UPDATE | T09 |
| RF-10 | Consultar um usuário específico (código) | SELECT | T10 |
| RF-11 | Consultar uma despesa específica (usuário + despesa) | SELECT | T10 |
| RF-12 | Consultar um investimento específico (usuário + investimento) | SELECT | T10 |
| RF-13 | Consultar todas as despesas do usuário, da mais recente à mais antiga | SELECT | T11 |
| RF-14 | Consultar todos os investimentos do usuário, do mais recente ao mais antigo | SELECT | T11 |
| RF-15 | Dashboard: usuário + última despesa + último investimento em **uma única linha** | SELECT | T12 |

### Não funcionais / regras do enunciado

| ID | Regra | Verificada em |
|---|---|---|
| RNF-01 | Banco Oracle | T05, T06, T13 |
| RNF-02 | Modelagem da Fase 3 como base; evoluções permitidas dentro do tema | T02, T03, T04 |
| RNF-03 | Máscaras: TEXTO → `'[NOME DO CAMPO]'`; NUMÉRICO → `[VALOR DO CAMPO]` | T08–T12, T14 |
| RNF-04 | Cada comando separado em seu respectivo item | T14 |
| RNF-05 | Alterações/consultas sempre filtradas pelo(s) código(s) (ID) | T09, T10, T13 |
| RNF-06 | Nomes aderentes às convenções do projeto (`T_SF_*`, `vl_`, `dt_`…) | T03, T06 |
| RNF-07 | Comandos específicos para as tabelas dos documentos do projeto | T03, T04, T14 |
| RNF-08 | Entrega em **PDF** (Word → PDF) com desenho(s) do modelo relacional + comandos | T04, T14 |

## 4. Decisões (detalhe em [T02](T02-decisoes-tecnicas.md))

Registro completo: [`docs/05-banco-de-dados/decisoes-tecnicas.md`](../docs/05-banco-de-dados/decisoes-tecnicas.md). **Todas aprovadas** (D-01, D-02, D-09, D-10 pela responsável; demais delegadas — critério: boas práticas).

| ID | Decisão |
|---|---|
| D-01 | Nova tabela `T_SF_INVESTIMENTO` |
| D-02 | IDs por `IDENTITY` → `INSERT` sem coluna de ID, igual aos exemplos do enunciado |
| D-03 | Datas: `TO_DATE('[DATA]', 'DD/MM/YYYY')`; datas de sistema com `SYSDATE` |
| D-04 | Domínios em maiúsculas, garantidos por `CHECK` |
| D-05 | Senha só como hash; nunca retornada nem alterada pelo UPDATE de perfil |
| D-06 | UPDATE completo das colunas editáveis; nunca PK/`id_usuario`/`senha`/datas de criação |
| D-07 | Comandos sem `COMMIT` (transação é da aplicação) |
| D-08 | "Mais recente" = `data DESC, id DESC` |
| D-09 | Validação em Oracle Free no Docker (WSL2); Oracle FIAP como plano B |
| D-10 | Entrega: Word → PDF com diagrama relacional + comandos |
| D-11 / D-12 | Dashboard: campos definidos; 1 linha com `LEFT JOIN` mesmo sem gasto/investimento |
| D-13 | E-mail único (`UNIQUE`) |
| D-14 | FK composta `(id_conta, id_usuario)`: conta do lançamento pertence ao mesmo usuário |
| D-15 | `T_SF_PARCELA.dt_pagamento` opcional |
| D-16 | SQL compatível com Oracle 19c |
| D-17 | Taxas como fração decimal (`0.0299` = 2,99%) |

## 5. Painel de tarefas

Status: `⬜ A fazer` · `🟨 Em andamento` · `🟥 Bloqueada` · `✅ Concluída`
Tamanho: **P** ≤ 1h · **M** 1–3h · **G** > 3h

| ID | Tarefa | Fase | Tam. | Depende de | Status |
|---|---|---|---|---|---|
| [T01](T01-preparacao-repositorio.md) | Preparação do repositório | A | P | — | 🟨 |
| [T02](T02-decisoes-tecnicas.md) | Decisões técnicas (ADR) | A | P | T01 | ✅ |
| [T03](T03-especificacao-modelo-dados.md) | Especificação do modelo (dicionário de dados) | A | M | T02 | ⬜ |
| [T04](T04-diagrama-relacional.md) | Atualização do diagrama relacional | B | M | T03 | ⬜ |
| [T05](T05-ambiente-oracle.md) | Ambiente Oracle local (Docker/WSL2) | B | M | T01 | ⬜ |
| [T06](T06-script-ddl.md) | Script DDL | B | M | T03 | ⬜ |
| [T07](T07-massa-de-dados-teste.md) | Massa de dados de teste + resultados esperados | B | M | T06 | ⬜ |
| [T08](T08-comandos-cadastro.md) | Comandos de cadastro (5 INSERT) | C | M | T03 | ⬜ |
| [T09](T09-comandos-alteracao.md) | Comandos de alteração (4 UPDATE) | C | P | T03 | ⬜ |
| [T10](T10-consultas-simples.md) | Consultas simples (3 SELECT) | C | P | T03 | ⬜ |
| [T11](T11-consultas-ordenadas.md) | Consultas ordenadas (2 SELECT) | C | P | T03 | ⬜ |
| [T12](T12-consulta-dashboard.md) | Consulta do dashboard (1 SELECT) | C | G | T03 | ⬜ |
| [T13](T13-validacao-oracle.md) | Validação no Oracle + evidências (**gate**) | D | G | T05–T12 | ⬜ |
| [T14](T14-documento-entrega.md) | Documento de entrega (Word → PDF) | E | M | T04, T13 | ⬜ |
| [T15](T15-documentacao-repositorio.md) | Atualização da documentação do repositório | E | P | T14 | ⬜ |
| [T16](T16-entrega-e-versionamento.md) | PR, merge, tag e envio no portal | E | P | T15 | ⬜ |

## 6. Grafo de dependências

```
T01 ─┬─► T02 ─► T03 ─┬─► T04 ───────────────────────────────┐
     │               ├─► T06 ─► T07 ────────┐                │
     │               ├─► T08 ─┐             │                │
     │               ├─► T09 ─┤             ▼                ▼
     │               ├─► T10 ─┼──────────► T13 (gate) ─────► T14 ─► T15 ─► T16
     │               ├─► T11 ─┤             ▲
     │               └─► T12 ─┘             │
     └─► T05 (ambiente, pode começar já) ───┘
```

Paralelismo: **T05** pode começar imediatamente; **T04, T06 e T08–T12** podem correr em paralelo após T03.
Caminho crítico: T01 → T02 → T03 → T12 → T13 → T14 → T15 → T16.

## 7. Matriz de rastreabilidade (requisito → item do PDF → testes)

| Req. | Item no documento de entrega | Casos de teste (T13) |
|---|---|---|
| RF-01 | 5.1 Cadastro — novo usuário | TC-C01, TC-C02 |
| RF-02 | 5.1 Cadastro — conta bancária | TC-C03, TC-C04 |
| RF-03 | 5.1 Cadastro — nova receita | TC-C05 |
| RF-04 | 5.1 Cadastro — nova despesa | TC-C06, TC-C07 |
| RF-05 | 5.1 Cadastro — novo investimento | TC-C08 |
| RF-06 | 5.2 Alteração — usuário | TC-A01, TC-A02 |
| RF-07 | 5.2 Alteração — receita | TC-A03, TC-A04 |
| RF-08 | 5.2 Alteração — despesa | TC-A05, TC-A06 |
| RF-09 | 5.2 Alteração — investimento | TC-A07 |
| RF-10 | 5.3 Consulta simples — usuário | TC-S01 |
| RF-11 | 5.3 Consulta simples — despesa | TC-S02, TC-S03 |
| RF-12 | 5.3 Consulta simples — investimento | TC-S04 |
| RF-13 | 5.4 Consulta ordenada — despesas | TC-O01 |
| RF-14 | 5.4 Consulta ordenada — investimentos | TC-O02 |
| RF-15 | 5.5 Dashboard | TC-D01 a TC-D06 |
| RNF-08 | 3. Modelo relacional (lógico + físico) | revisão visual (T14) |

## 8. Checklist de verificação da execução (gates por fase)

**Fase A — Fundação**
- [ ] PR do plano mergeado; branch `feat/sql-comandos` criada (T01)
- [x] Decisões D-01…D-17 resolvidas; nenhuma "Proposta" pendente (T02)
- [ ] Dicionário de dados publicado, cobrindo 10 tabelas e as evoluções da Fase 3 (T03)

**Fase B — Modelo e banco**
- [ ] Diagrama lógico + físico com `T_SF_INVESTIMENTO`, exportado em PNG/PDF legível (T04)
- [ ] Oracle local no ar; usuário `fintech` conecta; nenhuma senha no git (T05)
- [ ] DDL executa 2x seguidas sem erro; objetos `VALID`; constraints nomeadas (T06)
- [ ] Massa carregada; `resultados-esperados.md` escrito **antes** dos testes (T07)

**Fase C — Comandos**
- [ ] 15 comandos em `database/comandos/fintech-comandos.sql`, cada um com o título do enunciado (T08–T12)
- [ ] `INSERT` sem coluna de ID; máscaras: texto com aspas, número sem aspas, data com `TO_DATE`
- [ ] Todo `UPDATE` com `WHERE` pela PK (+ `id_usuario` em receita/despesa/investimento)
- [ ] Nenhum `SELECT *`; nenhuma consulta retorna `senha`
- [ ] Dashboard: `ROW_NUMBER`/`FETCH FIRST` + `LEFT JOIN` (sem produto cartesiano)

**Fase D — Validação (gate)**
- [ ] 100% dos TC-* com **Passou** (T13)
- [ ] Execução `00 → 01 → 02 → 03` reproduzida 2x sem diferença
- [ ] Equivalência máscara × comando testado confirmada para os 15 comandos
- [ ] Evidências em `database/testes/evidencias/`

**Fase E — Entrega**
- [ ] PDF com capa, modelo relacional (lógico + físico), convenção de máscaras e 15 comandos (T14)
- [ ] SQL do PDF ≡ `.sql` validado; sem aspas inteligentes (T14)
- [ ] `AGENTS.md` e `database/README.md` atualizados; dicionário ≡ DDL ≡ diagrama (T15)
- [ ] PR mergeado, tag `fase4-comandos-sql`, PDF enviado no portal (T16)

## 9. Definição de Pronto (global)

1. O PDF contém o modelo relacional atualizado e os 15 comandos, na ordem e com os títulos do enunciado.
2. Cada comando foi executado com valores reais em Oracle e passou nos seus casos de teste.
3. O repositório contém DDL, massa, testes e evidências reprodutíveis, e o gerador do documento.
4. A documentação reflete a nova estrutura; o trabalho está no `main` com tag.

## 10. Estrutura de artefatos ao final

```
projeto-fintech/
├── database/
│   ├── README.md                         # T05, T15
│   ├── .env.example                      # T05 (.env.local fica fora do git)
│   ├── ddl/00-drop-tables.sql            # T06
│   ├── ddl/01-create-tables.sql          # T06
│   ├── dml/02-seed.sql                   # T07
│   ├── comandos/fintech-comandos.sql     # T08–T12  ← fonte dos comandos do PDF
│   └── testes/
│       ├── resultados-esperados.md       # T07
│       ├── 03-testes-comandos.sql        # T13
│       └── evidencias/                   # T13
├── docs/
│   ├── 03-modelagem-de-dados/
│   │   ├── modelagem-de-dados.pdf        # Fase 3 (original, preservado)
│   │   ├── modelo-relacional.drawio      # fonte editável (T01/T04)
│   │   ├── modelo-logico-v2.png          # T04
│   │   ├── modelo-fisico-v2.png          # T04
│   │   └── modelagem-de-dados-v2.pdf     # T04
│   └── 05-banco-de-dados/
│       ├── orientacoes-atividade.txt     # enunciado
│       ├── decisoes-tecnicas.md          # T02
│       ├── dicionario-de-dados.md        # T03
│       └── entrega/                      # T14 — gerador, .docx e .pdf final
└── tasks/                                # este plano
```

## 11. Riscos principais

| Risco | Impacto | Mitigação |
|---|---|---|
| Professor esperar só as tabelas da Fase 3 | Médio | Seção "Evoluções" no PDF citando o trecho do enunciado que autoriza evoluir o modelo (T14) |
| SQL válido no 23ai e inválido no 19c da FIAP | Alto | D-16 + revisão dirigida; rodar DDL + dashboard no Oracle FIAP se houver acesso (T13) |
| Word converter `'` em `’` | Alto (SQL inválido) | Gerar o DOCX por script; diff do texto extraído do PDF (T14) |
| Docker/Oracle não subir no WSL2 | Médio | Plano B: Oracle FIAP (T05) |
| Dashboard retornar >1 linha ou perder usuário sem gasto | Alto | Especificação e 6 casos de teste dedicados (T12, T13) |
| Word/LibreOffice ausentes para gerar PDF | Médio | Instalar LibreOffice via winget ou usar Word Online (T14) |

## 12. Como manter este plano

- Iniciou uma tarefa: status `🟨` aqui **e** no cabeçalho do `Txx`.
- Concluiu: todos os critérios de aceitação do `Txx` marcados → `✅`.
- Mudou decisão ou escopo: registrar em T02 (nova `D-xx`) e ajustar as tarefas afetadas — nunca mudar o plano silenciosamente.
- Nova tarefa: copiar [`_TEMPLATE.md`](_TEMPLATE.md) e incluir nas seções 5 e 6.

## 13. Registro de execução

| Data | Evento |
|---|---|
| 2026-09-27 | Plano criado; D-01, D-02, D-09, D-10 aprovadas |
| 2026-09-27 | T02 concluída: D-03…D-17 decididas por boas práticas (delegado pela responsável); D-14 revisada para FK composta; D-17 criada; `decisoes-tecnicas.md` publicado |
