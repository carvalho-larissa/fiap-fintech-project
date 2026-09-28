# T04 — Atualização do diagrama relacional (Fase 3 → Fase 6)

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | M |
| Depende de | T03 |
| Bloqueia | T14 |
| Requisitos | D-10 (entrega exige o desenho do modelo relacional), RNF-02 |

## Objetivo
Produzir o desenho do **modelo relacional** atualizado (lógico e físico), incluindo `T_SF_INVESTIMENTO` e as correções aprovadas, pronto para ser colado no documento de entrega.

## Contexto
- A instrução de entrega exige: *"Anexe o(s) desenho(s) de seu modelo RELACIONAL que você criou na FASE 3."*
- Se o documento mostrar o desenho da Fase 3 **sem** a tabela de investimentos, os comandos de investimento não terão tabela correspondente no desenho → inconsistência visível para o avaliador.
- **Achado:** o PDF da Fase 3 foi gerado pelo draw.io e contém o arquivo editável embutido. Ele foi extraído para `docs/03-modelagem-de-dados/modelo-relacional.drawio` (2 páginas: *Modelo Lógico* e *Modelo Físico*). Não é preciso redesenhar do zero.

## Escopo
**Inclui:** edição do `.drawio`, exportação em PNG/PDF em alta resolução.
**Não inclui:** mudar layout/estilo das tabelas existentes (manter a identidade visual da Fase 3).

## Especificação
1. Abrir `modelo-relacional.drawio` no draw.io (desktop: `winget install JGraph.Draw` ou https://app.diagrams.net).
2. Em **ambas** as páginas, adicionar `T_SF_INVESTIMENTO` copiando o estilo de uma tabela existente (ex.: `T_SF_GASTO`):
   - colunas e tipos conforme D-01 (lógico: `NUMERIC`/`VARCHAR`/`Date`; físico: `NUMBER`/`VARCHAR2`/`DATE`)
   - asteriscos vermelhos nas colunas obrigatórias
   - relacionamentos: `T_SF_USUARIO 1 ─< N T_SF_INVESTIMENTO` e `T_SF_CONTA_BANCARIA 1 ─< N T_SF_INVESTIMENTO` (notação pé-de-galinha, igual às demais)
   - na página física: legendas `🔑 PK_T_SF_INVESTIMENTO (id_investimento)`, `🔗 FK_T_SF_USUARIO (id_usuario)`, `🔗 FK_T_SF_CONTA_BANCARIA (id_conta)`
3. Aplicar D-15: remover o asterisco de `T_SF_PARCELA.dt_pagamento`.
4. Atualizar os títulos para indicar a versão (ex.: "Modelo Físico — v2 (Fase 6)").
5. Exportar para `docs/03-modelagem-de-dados/`:
   - `modelo-logico-v2.png` e `modelo-fisico-v2.png` (escala ≥ 2x, fundo como o original)
   - `modelagem-de-dados-v2.pdf`
6. Manter o `modelagem-de-dados.pdf` original (histórico da Fase 3).

## Critérios de aceitação
- [ ] As duas páginas contêm `T_SF_INVESTIMENTO` com colunas, tipos e obrigatoriedade idênticos ao dicionário (T03)
- [ ] Relacionamentos com usuário e conta bancária desenhados com a cardinalidade correta
- [ ] Conferência cruzada diagrama × dicionário × DDL sem divergência (checagem feita em T13)
- [ ] PNGs legíveis quando colados em página A4 (testar zoom 100% no PDF final)
- [ ] `.drawio` editado versionado junto com os exports

## Artefatos de saída
- `docs/03-modelagem-de-dados/modelo-relacional.drawio` (fonte editável)
- `docs/03-modelagem-de-dados/modelo-logico-v2.png`
- `docs/03-modelagem-de-dados/modelo-fisico-v2.png`
- `docs/03-modelagem-de-dados/modelagem-de-dados-v2.pdf`

## Riscos e notas
- O diagrama tem fundo preto: em PDF impresso pode ficar pesado. Opcional: exportar também uma versão de fundo branco para o documento.
- Se a edição manual for inviável, o agente pode gerar o XML da nova tabela e inserir no `.drawio`, mas a revisão visual final é obrigatória.
