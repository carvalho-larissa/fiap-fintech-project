# T13 — Validação no Oracle + evidências (portão de qualidade)

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | G |
| Depende de | T05, T06, T07, T08, T09, T10, T11, T12 |
| Bloqueia | T14 |
| Requisitos | Todos os RF; RNF-01, RNF-05 |

## Objetivo
Provar, com execução real em Oracle, que **cada um dos 15 comandos** faz exatamente o que o enunciado pede. Nada entra no documento de entrega sem passar aqui.

## Contexto
Os comandos do entregável têm máscaras (`[VALOR DO GASTO]`) e **não executam** como estão. É preciso uma versão executável **estruturalmente idêntica** — só com os valores trocados — para que o teste valha para o que será entregue.

## Especificação
1. `database/testes/03-testes-comandos.sql`: para cada item do entregável, o mesmo comando com valores reais da massa (T07), seguido da verificação:
   - `INSERT`/`UPDATE`: `SQL%ROWCOUNT` esperado + `SELECT` de conferência
   - consultas: resultado comparado com `resultados-esperados.md`
   - casos negativos (TC-C02, C04, C07, A02): bloco que **espera** o erro Oracle correspondente
   - envolver cada bloco em `SAVEPOINT`/`ROLLBACK TO` para que a ordem dos testes não interfira
2. **Verificação de equivalência máscara × teste** (automatizável): substituir no teste cada valor pela máscara correspondente e comparar com o entregável — devem ficar idênticos exceto espaços. Alternativa manual: checklist lado a lado.
3. Execução completa, na ordem: `00-drop` → `01-create` → `02-seed` → `03-testes`, **duas vezes** (garante reprodutibilidade).
4. Registrar evidências em `database/testes/evidencias/`:
   - log/saída completa da execução (`execucao-AAAA-MM-DD.log`)
   - relatório `relatorio-testes.md`: tabela TC-ID | esperado | obtido | Passou/Falhou
   - capturas das consultas 4.1, 4.2 e 5 (úteis para o documento de entrega, opcional no PDF)
5. Se possível, executar também no Oracle FIAP (19c) ao menos o DDL + dashboard, para confirmar D-16.

## Critérios de aceitação
- [ ] 100% dos casos TC-C*, TC-A*, TC-S*, TC-O*, TC-D* com resultado **Passou**
- [ ] Execução completa reproduzida 2x sem diferença
- [ ] Equivalência máscara × teste confirmada para os 15 comandos
- [ ] Nenhum erro inesperado no log
- [ ] Qualquer falha gerou correção na tarefa de origem (T06–T12) e reexecução completa

## Artefatos de saída
- `database/testes/03-testes-comandos.sql`
- `database/testes/evidencias/relatorio-testes.md`
- `database/testes/evidencias/execucao-*.log`

## Riscos e notas
- Validar em 23ai e entregar para 19c: se não houver acesso ao Oracle FIAP, revisar manualmente contra a lista de D-16.
- Regra dos 2 erros: se o mesmo teste falhar 2x pelo mesmo motivo, parar e revisar a especificação (T03/T02), não o sintoma.
