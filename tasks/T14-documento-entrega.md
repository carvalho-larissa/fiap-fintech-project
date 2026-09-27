# T14 — Documento de entrega (Word → PDF)

| Campo | Valor |
|---|---|
| Status | ⬜ A fazer |
| Tamanho | M |
| Depende de | T04, T13 |
| Bloqueia | T15, T16 |
| Requisitos | D-10, RNF-03, RNF-04 |

## Objetivo
Montar o documento oficial exigido pela FIAP e exportá-lo para PDF.

## Contexto — instrução oficial de entrega
> Crie um documento no Word ou no processador de textos de sua preferência.
> Anexe o(s) desenho(s) de seu modelo RELACIONAL que você criou na FASE 3.
> Cole os comandos SQL solicitados no documento.
> Exporte o arquivo para PDF. [...] **É obrigatório exportar para PDF.**

Ambiente atual: **Word e LibreOffice não estão instalados** nesta máquina. O DOCX pode ser gerado por script (`python-docx`, via `uv`), mas a conversão para PDF exige Word, LibreOffice (`winget install TheDocumentFoundation.LibreOffice`) ou Word Online/Google Docs.

## Especificação
**Fonte única:** os comandos colados no documento vêm de `database/comandos/fintech-comandos.sql` já validado em T13 — **nunca** redigitados à mão.

Estrutura do documento:
1. **Capa** — FIAP · Atividade Fintech (Fase 4) · Larissa Gomes de Carvalho · RM 571266 · Turma 1TDSOA · data.
2. **Introdução** (curta) — objetivo da atividade e SGBD utilizado (Oracle).
3. **Modelo relacional**
   - 3.1 Modelo lógico (imagem de T04)
   - 3.2 Modelo físico (imagem de T04)
   - 3.3 Evoluções em relação à Fase 3 — tabela curta: `T_SF_INVESTIMENTO` (D-01), `IDENTITY` (D-02), `dt_pagamento` opcional (D-15), constraints de domínio (D-04); citar o trecho do enunciado que autoriza a evolução.
4. **Convenção das máscaras** — 3 linhas: texto `'[CAMPO]'`, número `[CAMPO]`, data `TO_DATE('[DATA]', 'DD/MM/YYYY')`.
5. **Comandos SQL** — uma subseção por item, **com o título exato do enunciado**:
   - 5.1 Cadastro (5) · 5.2 Alteração (4) · 5.3 Consultas simples (3) · 5.4 Consultas ordenadas (2) · 5.5 Consulta para o dashboard (1)
   - SQL em fonte monoespaçada (Consolas/Courier 9–10 pt), bloco com fundo cinza claro, sem quebra de linha no meio de palavras.
6. *(Opcional)* **Anexo — evidências de teste**: resumo do relatório de T13 (tabela de casos Passou) e captura do dashboard.

Arquivos:
- Gerador: `docs/05-banco-de-dados/entrega/gerar_documento.py` (monta o DOCX a partir do `.sql` e das imagens → reprodutível)
- `docs/05-banco-de-dados/entrega/Fintech-Fase4-Comandos-SQL-RM571266.docx`
- `docs/05-banco-de-dados/entrega/Fintech-Fase4-Comandos-SQL-RM571266.pdf` ← **arquivo enviado ao portal**

## Critérios de aceitação
- [ ] PDF abre corretamente e contém capa, diagrama(s) e os 15 comandos
- [ ] Diagramas legíveis em zoom 100% (tabelas e colunas lidas sem esforço)
- [ ] Os 15 títulos batem, na ordem, com o enunciado (checklist em `tasks/README.md` seção 7)
- [ ] Conteúdo SQL do PDF idêntico ao `.sql` validado (conferência por extração de texto do PDF + diff)
- [ ] Nenhuma máscara quebrada entre linhas/páginas de forma ilegível; aspas retas `'` (não "aspas inteligentes" ‘ ’ do Word)
- [ ] Nome do arquivo identifica aluna e atividade

## Artefatos de saída
- `docs/05-banco-de-dados/entrega/gerar_documento.py`
- `docs/05-banco-de-dados/entrega/*.docx` e `*.pdf`

## Riscos e notas
- **Aspas inteligentes**: o Word troca `'` por `’` ao colar/digitar — o SQL deixa de ser válido. Desligar a AutoCorreção ou gerar via script.
- Diagrama com fundo preto consome tinta e pode ficar escuro no PDF; considerar a versão de fundo branco (T04).
