# T16 — PR, merge, tag e envio no portal

| Campo | Valor |
|---|---|
| Status | ✅ Concluída |
| Tamanho | P |
| Depende de | T15 |
| Bloqueia | — (fim do plano) |
| Requisitos | — (entrega) |

## Objetivo
Integrar o trabalho ao `main` de forma rastreável e enviar o PDF à FIAP.

## Especificação
1. Commits pequenos e descritivos ao longo da execução (sugestão: um por tarefa, prefixo `feat(db):`, `docs:`, `test(db):`).
2. Abrir PR `feat/sql-comandos` → `main` com descrição contendo:
   - resumo do escopo (15 comandos + evolução do modelo)
   - decisões relevantes (D-01, D-02, D-10) com link para `decisoes-tecnicas.md`
   - link para `relatorio-testes.md` (evidência de validação)
   - checklist da seção 7 de `tasks/README.md`
3. Revisão final pela responsável (ler o PDF inteiro, não só o código).
4. Merge (squash ou merge commit — manter o histórico por tarefa é preferível: **merge commit**).
5. Tag anotada: `git tag -a fase6-comandos-sql -m "Entrega Fase 6 - Comandos SQL"` + `git push origin --tags`.
6. Enviar o PDF de T14 no portal FIAP; registrar data/hora do envio em `tasks/README.md`.

## Critérios de aceitação
- [x] PRs #2, #3, #5 e #6 mergeados no `main`; branches remotas de trabalho removidas
- [x] Tag `fase6-comandos-sql` no GitHub apontando para o merge do PR #6 (`bbe23f8`)
- [x] PDF enviado no portal FIAP em 2026-09-27 (confirmação da responsável)
- [x] Todos os status do painel em `tasks/README.md` = ✅

## Artefatos de saída
- PR no GitHub · tag `fase6-comandos-sql` · comprovante de envio

## Encerramento
- PR #6, com a correção de identificação para Fase 6, foi mergeado no `main` em 2026-09-28 UTC.
- A tag anotada `fase6-comandos-sql` aponta para o commit de merge `bbe23f8`.
- O PDF foi enviado ao portal FIAP em 2026-09-27, confirmado pela responsável.
