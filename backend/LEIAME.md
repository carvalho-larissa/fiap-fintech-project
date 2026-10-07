# Sistema Fintech — DAO + JDBC (Fase 7)

Larissa Gomes de Carvalho — RM 571266 — 1TDSOA (entrega individual)

Projeto IntelliJ (Java 21) com acesso ao Oracle da FIAP via JDBC.

## O que foi implementado
- **DAOs** com `insert()` e `getAll()`: `UsuarioDAO`, `GastoDAO`, `InvestimentoDAO` (as 3 entidades da atividade)
  e `ContaBancariaDAO`, `CategoriaDAO` (apoio às chaves estrangeiras).
- **Tratamento de exceções** com try-catch: `SQLException` vira `DaoException` com mensagem clara
  (banco fora do ar, tabela inexistente, e-mail duplicado, valor inválido, referência inexistente).
- **`Teste.java`**: insere 5 usuários, 5 gastos e 5 investimentos, chama `getAll()` e exibe o resultado;
  depois provoca 5 falhas de propósito para mostrar o tratamento de exceções.

## Como executar
**IntelliJ:** abrir esta pasta, escolher o JDK 17 ou 21 e executar `Teste` (ou `Main`, que não usa o banco).
A conexão está em `db.properties` (host `ORACLE.FIAP.COM.BR`, porta 1521, SID `ORCL`).

**Terminal (Java 17 ou 21), dentro desta pasta:**
```
javac -encoding UTF-8 -cp "lib/*" -d out src/*.java
java -cp "out;lib/ojdbc11.jar" Teste
```
(Linux/macOS: use `:` no lugar de `;`.) O `Teste` termina com o resumo
`N verificações, 0 falha(s)`.

O schema (10 tabelas `T_SF_*`) já existe na instância da FIAP. Cada execução do `Teste` grava novos
registros (e-mails únicos por horário).
