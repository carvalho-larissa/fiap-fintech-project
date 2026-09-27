# database/ — Banco de dados Oracle do Sistema Fintech

Scripts, comandos e testes da camada de dados. Modelo documentado em
[`docs/05-banco-de-dados/dicionario-de-dados.md`](../docs/05-banco-de-dados/dicionario-de-dados.md);
decisões em [`decisoes-tecnicas.md`](../docs/05-banco-de-dados/decisoes-tecnicas.md).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `ddl/00-drop-tables.sql` | Remove as 10 tabelas (idempotente, compatível com 19c) |
| `ddl/01-create-tables.sql` | Cria tabelas, constraints nomeadas, índices e comentários |
| `dml/02-seed.sql` | Massa de dados determinística para testes |
| `comandos/fintech-comandos.sql` | **Entregável**: os 15 comandos com máscaras de substituição |
| `testes/resultados-esperados.md` | Oráculo: resultados esperados de cada caso de teste |
| `testes/verificar_estatico.py` | Verificação sem banco (contrato DDL × dicionário × comandos) |
| `testes/executar_testes.py` | Executa os scripts e a suíte contra o Oracle; gera evidências |
| `testes/testes_constraints.py` | Testes negativos das constraints + revisão de compatibilidade 19c |
| `testes/evidencias/` | Relatório e log da última execução |
| `scripts/aguardar-oracle.sh` | Espera o container ficar pronto |
| `.env.example` | Modelo de credenciais (o real, `.env.local`, fica fora do git) |

Ordem de execução: `00` → `01` → `02` → comandos/testes.

## Ambiente local (Oracle Free em Docker no WSL2)

Pré-requisito: Docker Engine no Ubuntu do WSL (`sudo apt install docker.io`, usuário no grupo `docker`).

```bash
# 1. Credenciais locais (não versionadas)
cp database/.env.example database/.env.local   # e preencha as senhas

# 2. Container (dentro do WSL) — primeira vez
docker run -d --name oracle-fintech -p 1521:1521 \
  -e ORACLE_PASSWORD=<ORACLE_SYS_PASSWORD> \
  -e APP_USER=fintech -e APP_USER_PASSWORD=<ORACLE_PASSWORD> \
  -v oracle-fintech-data:/opt/oracle/oradata \
  gvenzl/oracle-free:23-slim

# Próximas vezes
docker start oracle-fintech
bash database/scripts/aguardar-oracle.sh
```

Conexão: `localhost:1521/FREEPDB1`, usuário `fintech` (acessível do Windows e do WSL).

**Armadilhas conhecidas**
- O WSL desliga a VM quando não há processo ativo e o container para junto. Mantenha um terminal WSL aberto durante os testes.
- Se o container foi criado e parado antes de terminar a primeira inicialização, as senhas do `docker run` podem não ter sido aplicadas (`ORA-01017`). Corrija sem recriar:
  `docker exec oracle-fintech resetPassword <sys>` e `docker exec oracle-fintech createAppUser fintech <senha> FREEPDB1`.
- A imagem é Oracle 23ai/26ai; o SQL do projeto é mantido compatível com 19c (FIAP) — ver D-16 e `TC-V01`.

## Rodando os testes (do Windows, na raiz do repositório)

```bash
uv run --with sqlglot  python database/testes/verificar_estatico.py        # sem banco
uv run --with oracledb python database/testes/executar_testes.py tudo      # recria o schema e testa
```

`tudo` = recria o schema (`00`→`01`→`02`) + estrutura + 40 casos funcionais + 10 de constraints/compatibilidade.
Casos que alteram dados rodam dentro de `SAVEPOINT`/`ROLLBACK`, então a ordem não interfere e a execução é repetível.
Resultado em `testes/evidencias/relatorio-testes.md`.
