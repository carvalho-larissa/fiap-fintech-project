# T05 — Ambiente Oracle local (Docker no WSL2)

| Campo | Valor |
|---|---|
| Status | ⬜ A fazer |
| Tamanho | M |
| Depende de | T01 |
| Bloqueia | T07 (execução), T08, T13 |
| Requisitos | RNF-01, D-09 |

## Objetivo
Ter um Oracle rodando localmente, reproduzível com um comando, para validar DDL e comandos sem depender do servidor da FIAP.

## Contexto (levantado nesta máquina)
- Windows 11; **WSL2 com Ubuntu 24.04 já instalado**.
- Docker **não** instalado; `sqlplus` **não** instalado.
- Java 26 e Python/uv disponíveis no Windows.

## Escopo
**Inclui:** instalação do Docker, container Oracle, cliente para executar scripts, arquivo de credenciais local.
**Não inclui:** configuração do Oracle da FIAP (plano B, ver notas).

## Especificação
1. **Docker** — escolher uma opção:
   - (A) Docker Engine dentro do Ubuntu/WSL2: `sudo apt install docker.io` + `sudo usermod -aG docker $USER` (mais leve, sem licença).
   - (B) Docker Desktop para Windows com backend WSL2 (`winget install Docker.DockerDesktop`) — mais simples, exige reinício.
2. **Container** (imagem oficial gratuita, sem login):
   ```bash
   docker run -d --name oracle-fintech \
     -p 1521:1521 \
     -e ORACLE_PASSWORD=<senha-local> \
     -e APP_USER=fintech -e APP_USER_PASSWORD=<senha-app> \
     -v oracle-fintech-data:/opt/oracle/oradata \
     gvenzl/oracle-free:23-slim
   ```
   Aguardar o log `DATABASE IS READY TO USE!`.
3. **Cliente para rodar scripts** (qualquer um):
   - `docker exec -i oracle-fintech sqlplus fintech/<senha-app>@FREEPDB1 < script.sql`
   - ou `python-oracledb` (modo thin, sem instalar client) via `uv run --with oracledb`
   - ou SQL Developer / extensão Oracle SQL Developer para VS Code (visual, bom para evidências).
4. **Credenciais**: `database/.env.local` (ignorado pelo git) com `ORACLE_DSN=localhost:1521/FREEPDB1`, `ORACLE_USER=fintech`, `ORACLE_PASSWORD=…`.
5. Documentar o passo a passo em `database/README.md` (seção "Ambiente local").

## Critérios de aceitação
- [ ] `SELECT banner FROM v$version` retorna a versão do Oracle Free
- [ ] Usuário `fintech` conecta em `localhost:1521/FREEPDB1`
- [ ] Container reinicia sem perda de dados (volume nomeado)
- [ ] Nenhuma senha em arquivo versionado (`git grep -i password` limpo, exceto placeholders)
- [ ] Passo a passo reproduzível documentado

## Artefatos de saída
- `database/README.md` (seção ambiente)
- `database/.env.example` (placeholders, versionado) · `database/.env.local` (real, **não** versionado)

## Riscos e notas
- Imagem ~1,5 GB e ~2 GB de RAM em uso; fechar o container após a validação (`docker stop oracle-fintech`).
- Oracle 23ai aceita sintaxes que o 19c (FIAP) rejeita → respeitar D-16 ao escrever o SQL.
- **Plano B**: Oracle FIAP (`oracle.fiap.com.br:1521/ORCL`, usuário `RM571266`). Antes de rodar o `DROP` do DDL lá, verificar se existem tabelas da Fase 3 que precisam ser preservadas.
