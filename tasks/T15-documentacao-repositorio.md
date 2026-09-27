# T15 — Atualização da documentação do repositório

| Campo | Valor |
|---|---|
| Status | ⬜ A fazer |
| Tamanho | P |
| Depende de | T14 |
| Bloqueia | T16 |
| Requisitos | — (governança do repositório) |

## Objetivo
Deixar o repositório consistente com o novo estado do projeto, para que a próxima fase (Java + JDBC) comece sem redescoberta.

## Especificação
1. **`AGENTS.md`**
   - Árvore de diretórios com `database/`, `docs/05-banco-de-dados/`, `tasks/` e os novos arquivos de `docs/03-modelagem-de-dados/`.
   - Tabela de rastreabilidade: incluir linha de **Investimentos** (`T_SF_INVESTIMENTO` — sem classe Java ainda — sem tela ainda).
   - Seção "Como executar" → banco: subir container + ordem dos scripts (`00` → `01` → `02` → `03`).
   - Convenções: IDENTITY, máscaras, domínios em maiúsculas, nada de `SELECT *`.
   - Lacunas conhecidas atualizadas (ex.: `Investimento.java` inexistente; front sem tela de investimentos).
2. **`database/README.md`** — propósito de cada script, ordem de execução, ambiente (de T05), como rodar os testes.
3. **Conferência cruzada** (checklist): dicionário (T03) ≡ DDL (T06) ≡ diagrama (T04) — mesmas tabelas, colunas, tipos e obrigatoriedade.
4. **`.gitignore`** — `database/.env.local`, arquivos temporários do Word (`~$*.docx`, já coberto).
5. *(Opcional, recomendado para a próxima fase)* Registrar em `tasks/README.md` → "Próximos passos": criar `Investimento.java`, alinhar tipos Java (`double` → `BigDecimal` para dinheiro), DAO com `PreparedStatement` usando exatamente os comandos deste entregável (as máscaras viram `?`).

## Critérios de aceitação
- [ ] `AGENTS.md` descreve todos os diretórios e arquivos novos
- [ ] Conferência cruzada dicionário × DDL × diagrama sem divergência
- [ ] Nenhum link quebrado entre documentos (`tasks/`, `docs/`, `database/`)

## Artefatos de saída
- `AGENTS.md`, `database/README.md`, `.gitignore` (atualizados)
