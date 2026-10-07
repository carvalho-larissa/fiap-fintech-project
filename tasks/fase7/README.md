# Plano de Tarefas — Fase 7: DAO + JDBC com Oracle FIAP

Enunciado: [`docs/01-requisitos/nova-atividade.md`](../../docs/01-requisitos/nova-atividade.md).
Entidades: **Usuario, Gasto, Investimento** (+ `ContaBancariaDAO` como apoio às FKs).
Entrega: ZIP `GRUPO_XX.zip` exportado do IntelliJ; validar que o projeto executa sem erros antes de enviar.
Branch: `feat/dao-jdbc`. Plano completo: ver J01–J13 abaixo.

Status: `⬜ A fazer` · `🟨 Em andamento` · `🟥 Bloqueada` · `✅ Concluída`

| ID | Tarefa | Status |
|---|---|---|
| J01 | Ambiente Java 17/21 e driver ojdbc11 | ✅ |
| J02 | Obter e validar acesso à instância Oracle FIAP | ✅ |
| J03 | Schema na FIAP (categorias saíram do SQL: `Teste` as cria via `CategoriaDAO`) | ✅ |
| J04 | `ConnectionFactory` + `DaoException` | ✅ |
| J05 | Ajustar entidades (`Gasto`, nova `Investimento`, `Categoria`) | ✅ |
| J06 | `UsuarioDAO` (molde) | ✅ |
| J07 | `Teste.java` com Usuario | ✅ |
| J08 | `ContaBancariaDAO` (+ `CategoriaDAO`) | ✅ |
| J09 | `GastoDAO` + teste | ✅ |
| J10 | `InvestimentoDAO` + teste | ✅ |
| J11 | Cenários de exceção no `Teste` | ✅ (5 cenários; senha errada ficou de fora de propósito) |
| J12 | Execução na FIAP + evidências | ✅ |
| J13 | Documentação, checklist e preparação do ZIP | ✅ |

## Notas de execução
- J01: language level 21, `ojdbc11.jar` 23.9 em `backend/lib/` (SHA-1 conferido) e registrado no `.iml`; `javac --release 17` e `--release 21` compilam as classes atuais. Só há JDK 26 na máquina — instalar JDK 21 para validar de verdade.
- Entrega em ZIP: credenciais da FIAP não podem ir no ZIP; definir em J02/J13 como o projeto lê a config sem expor senha.
- J01–J10 (2026-10-07): JDK 21 (Temurin 21.0.12) instalado; `Teste` roda com JDK 21 contra o Oracle local (Docker): 13 verificações, 0 falhas; compila também com `--release 17`. Tudo fora a FIAP está pronto — faltam J02/J03 (acesso e schema na FIAP), J12 (execução + evidências lá) e J13.
- Mudanças vs. plano: `CategoriaDAO` substitui o script `03-prerequisitos-dao.sql` (o `Teste` garante as categorias, então roda em qualquer schema); credenciais via `DB_URL/DB_USER/DB_PASSWORD` ou `backend/db.properties` (ignorado pelo git; modelo `db.properties.example`).
- Execução (Windows, a partir de `backend/`): `javac -encoding UTF-8 -cp "lib/*" -d out src/*.java` e `java -cp "out;lib/ojdbc11.jar" Teste`.
- J02/J03/J12 (2026-10-07): conexão com `ORACLE.FIAP.COM.BR:1521:ORCL` (Oracle 19c, usuário = RM) funcionou. Schema da FIAP estava vazio; `01-create-tables.sql` criou as 10 tabelas (57 constraints nomeadas, 0 objetos inválidos), sem rodar o `00-drop`. `Teste` na FIAP: 13 verificações, 0 falhas — evidência em `docs/06-java-jdbc/evidencias/execucao-teste-fiap.md`.
- Cenário "senha errada" não foi automatizado: cada tentativa inválida conta para o bloqueio da conta (ORA-28000) na instância compartilhada da FIAP.
- Atenção: cada execução do `Teste` grava novos registros no schema da FIAP (e-mails únicos por timestamp); não há DELETE no escopo.
- J13 (2026-10-07): `AGENTS.md` e `backend/LEIAME.md` atualizados. ZIP `RM571266.zip` (entrega individual) gerado a partir de `backend/` (sem `out/` nem `workspace.xml`, **com** `db.properties`) e validado extraindo em pasta limpa: compila com JDK 21 e `Teste` roda na FIAP com 13 verificações, 0 falhas.

## Checklist final contra o enunciado
- [x] Classe DAO acessando o Oracle (`UsuarioDAO`, `GastoDAO`, `InvestimentoDAO`)
- [x] `getAll()` com SELECT → `List` de objetos
- [x] `insert()` com INSERT; `Teste.main()` cadastra 5 registros por entidade e chama `getAll()`
- [x] Tratamento de exceções com try-catch (`DaoException`; banco fora do ar, tabela inexistente etc.)
- [x] Classe de teste com método `main`
- [x] 3 entidades (Usuario, Gasto, Investimento) da modelagem do FINTECH
- [x] Java 21; Oracle da FIAP (19c, `ORACLE.FIAP.COM.BR:1521:ORCL`)
- [x] ZIP nomeado com o RM; projeto validado executando sem erros
