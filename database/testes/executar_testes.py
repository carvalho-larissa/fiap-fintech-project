"""
Executor de scripts SQL e da suíte de testes da Fase 4 contra Oracle (T13).

- Lê credenciais de database/.env.local (fora do git).
- Executa scripts .sql (DDL/DML) dividindo por ';' e por '/' (blocos PL/SQL).
- Executa a suíte: cada comando do ENTREGÁVEL é carregado de fintech-comandos.sql,
  as máscaras são substituídas por valores reais (sem reescrever o comando — prova de
  equivalência máscara x teste) e o resultado é comparado ao oráculo.
- Casos que alteram dados rodam dentro de SAVEPOINT + ROLLBACK (isolados entre si).
- Gera relatório Markdown e log em database/testes/evidencias/.

Uso:
  uv run --with oracledb python database/testes/executar_testes.py setup     # 00 -> 01 -> 02
  uv run --with oracledb python database/testes/executar_testes.py testes    # suíte
  uv run --with oracledb python database/testes/executar_testes.py tudo      # setup + testes
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

import oracledb

RAIZ = Path(__file__).resolve().parents[2]
ENV = RAIZ / "database/.env.local"
SCRIPTS = [
    RAIZ / "database/ddl/00-drop-tables.sql",
    RAIZ / "database/ddl/01-create-tables.sql",
    RAIZ / "database/dml/02-seed.sql",
]
COMANDOS = RAIZ / "database/comandos/fintech-comandos.sql"
EVID = RAIZ / "database/testes/evidencias"

LOG: list[str] = []


def log(msg: str = ""):
    print(msg)
    LOG.append(msg)


def conectar():
    cfg = dict(l.split("=", 1) for l in ENV.read_text().split() if "=" in l)
    return oracledb.connect(user=cfg["ORACLE_USER"], password=cfg["ORACLE_PASSWORD"], dsn=cfg["ORACLE_DSN"])


# ---------------------------------------------------------------------------
# Execução de scripts
# ---------------------------------------------------------------------------
def dividir_script(sql: str) -> list[str]:
    """Divide um script SQL*Plus em comandos: blocos PL/SQL terminam em '/', o resto em ';'."""
    cmds, buf, em_bloco = [], [], False
    for linha in sql.splitlines():
        s = linha.strip()
        su = s.upper()
        if not buf and (not s or s.startswith("--") or su.startswith(("SET ", "PROMPT", "SPOOL"))):
            continue
        if not buf and re.match(r"^(DECLARE|BEGIN)\b", su):
            em_bloco = True
        if em_bloco:
            if s == "/":
                cmds.append("\n".join(buf).strip())
                buf, em_bloco = [], False
            else:
                buf.append(linha)
            continue
        buf.append(linha)
        sem_coment = re.sub(r"--.*$", "", linha).rstrip()
        if sem_coment.endswith(";"):
            texto = "\n".join(buf).strip()
            texto = re.sub(r";\s*(--[^\n]*)?$", "", texto)
            cmds.append(texto)
            buf = []
    if "".join(buf).strip():
        cmds.append("\n".join(buf).strip())
    return [c for c in cmds if re.sub(r"--[^\n]*", "", c).strip()]


def executar_script(con, arq: Path):
    cur = con.cursor()
    cur.callproc("DBMS_OUTPUT.ENABLE")
    cmds = dividir_script(arq.read_text(encoding="utf-8"))
    log(f"\n### {arq.relative_to(RAIZ).as_posix()} — {len(cmds)} comandos")
    for i, c in enumerate(cmds, 1):
        try:
            cur.execute(c)
        except oracledb.DatabaseError as e:
            log(f"ERRO no comando {i}: {e}\n{c[:300]}")
            raise
    con.commit()
    # saída DBMS_OUTPUT (script de drop)
    linha, status = cur.var(str), cur.var(int)
    while True:
        cur.callproc("DBMS_OUTPUT.GET_LINE", (linha, status))
        if status.getvalue() != 0:
            break
        log(f"    {linha.getvalue()}")
    log(f"OK: {len(cmds)} comandos executados")


def setup(con):
    for s in SCRIPTS:
        executar_script(con, s)


# ---------------------------------------------------------------------------
# Comandos do entregável
# ---------------------------------------------------------------------------
def carregar_comandos() -> dict[str, str]:
    texto = COMANDOS.read_text(encoding="utf-8")
    blocos = re.split(r"^-- (\d\.\d) .*$", texto, flags=re.M)
    cmds = {}
    for i in range(1, len(blocos), 2):
        corpo = re.sub(r"--[^\n]*", "", blocos[i + 1])
        corpo = corpo.split(";")[0].strip()
        cmds[blocos[i]] = corpo
    assert len(cmds) == 15, f"esperava 15 comandos, achei {len(cmds)}"
    return cmds


def preencher(cmd: str, valores: dict[str, object]) -> str:
    """Troca cada máscara pelo literal SQL correspondente. Máscara sem valor = erro."""

    def lit(v):
        if v is None:
            return "NULL"
        if isinstance(v, str):
            return v.replace("'", "''")
        return str(v)

    def troca_texto(m):
        chave = m.group(1)
        v = valores[chave]
        return "NULL" if v is None else f"'{lit(v)}'"

    def troca_data(m):
        chave = m.group(1)
        v = valores[chave]
        return "NULL" if v is None else f"TO_DATE('{v}', 'DD/MM/YYYY')"

    cmd = re.sub(r"TO_DATE\('\[([^\]]+)\]', 'DD/MM/YYYY'\)", troca_data, cmd)
    cmd = re.sub(r"'\[([^\]]+)\]'", troca_texto, cmd)
    cmd = re.sub(r"\[([^\]]+)\]", lambda m: lit(valores[m.group(1)]), cmd)
    assert "[" not in cmd, f"máscara não substituída: {cmd}"
    return cmd


# ---------------------------------------------------------------------------
# Suíte
# ---------------------------------------------------------------------------
@dataclass
class Resultado:
    caso: str
    descricao: str
    esperado: str
    obtido: str
    passou: bool


RESULTADOS: list[Resultado] = []


def registrar(caso, descricao, esperado, obtido, passou):
    RESULTADOS.append(Resultado(caso, descricao, str(esperado), str(obtido), passou))
    log(f"  [{'PASSOU' if passou else 'FALHOU'}] {caso} — {descricao} | esperado: {esperado} | obtido: {obtido}")


def normalizar(v):
    if isinstance(v, dt.datetime):
        return v.strftime("%d/%m/%Y")
    if isinstance(v, float):
        return Decimal(str(v)).normalize()
    if isinstance(v, Decimal) and v == v.to_integral_value():
        return int(v)
    return v


def consulta(cur, sql):
    cur.execute(sql)
    cols = [d[0].lower() for d in cur.description]
    return cols, [tuple(normalizar(v) for v in r) for r in cur.fetchall()]


def em_savepoint(con, fn):
    cur = con.cursor()
    cur.execute("SAVEPOINT sp_teste")
    try:
        return fn(cur)
    finally:
        cur.execute("ROLLBACK TO SAVEPOINT sp_teste")


def espera_erro(cur, sql, ora: str, constraint: str):
    try:
        cur.execute(sql)
        return False, "nenhum erro"
    except oracledb.DatabaseError as e:
        msg = str(e)
        ok = ora in msg and constraint.upper() in msg.upper()
        return ok, msg.splitlines()[0]


def suite(con):
    C = carregar_comandos()
    oracledb.defaults.fetch_decimals = True
    cur = con.cursor()

    # ------------------------------------------------------------------ 1. Cadastro
    log("\n## 1. Cadastro")
    usuario_ok = {"NOME DO USUÁRIO": "Eva Lima", "E-MAIL DO USUÁRIO": "eva@exemplo.com",
                  "HASH DA SENHA": "$2a$10$hashficticio.eva", "CAMINHO DO AVATAR": "avatars/eva.png"}

    def tc_c01(cur):
        cur.execute(preencher(C["1.1"], usuario_ok))
        n = cur.rowcount
        _, r = consulta(cur, "SELECT id_usuario, CASE WHEN TRUNC(dt_cadastro) = TRUNC(SYSDATE) THEN 'hoje' END, ativo "
                             "FROM T_SF_USUARIO WHERE email = 'eva@exemplo.com'")
        return n, r
    n, r = em_savepoint(con, tc_c01)
    registrar("TC-C01", "novo usuário válido", "1 linha; id 5; dt_cadastro hoje; ativo S",
              f"{n} linha; {r}", n == 1 and r == [(5, "hoje", "S")])

    ok, msg = em_savepoint(con, lambda cur: espera_erro(
        cur, preencher(C["1.1"], {**usuario_ok, "E-MAIL DO USUÁRIO": "larissa@exemplo.com"}),
        "ORA-00001", "UK_SF_USUARIO_EMAIL"))
    registrar("TC-C02", "e-mail duplicado", "ORA-00001 UK_SF_USUARIO_EMAIL", msg, ok)

    conta = {"CÓDIGO DO USUÁRIO": 4, "NOME DO BANCO": "Santander", "TIPO DA CONTA": "CORRENTE",
             "NÚMERO DA CONTA": "4444-4"}
    r = em_savepoint(con, lambda cur: (cur.execute(preencher(C["1.2"], conta)), cur.rowcount, consulta(
        cur, "SELECT id_conta, ativa FROM T_SF_CONTA_BANCARIA WHERE nr_conta = '4444-4'")[1]))
    registrar("TC-C03", "conta para usuário existente", "1 linha; id 6; ativa S", f"{r[1]}; {r[2]}",
              r[1] == 1 and r[2] == [(6, "S")])

    ok, msg = em_savepoint(con, lambda cur: espera_erro(
        cur, preencher(C["1.2"], {**conta, "CÓDIGO DO USUÁRIO": 999}), "ORA-02291", "FK_SF_CONTA_USUARIO"))
    registrar("TC-C04", "conta para usuário inexistente", "ORA-02291 FK_SF_CONTA_USUARIO", msg, ok)

    receita = {"CÓDIGO DO USUÁRIO": 1, "CÓDIGO DA CONTA": 1, "CÓDIGO DA CATEGORIA": 2,
               "DESCRIÇÃO DA RECEITA": "Consultoria", "VALOR DA RECEITA": "750.00",
               "DATA DO RECEBIMENTO": "20/10/2025", "ORIGEM DA RECEITA": "FREELANCE",
               "RECORRÊNCIA DA RECEITA": "UNICA", "CAMINHO DO COMPROVANTE": "comprovantes/r3.pdf"}
    r = em_savepoint(con, lambda cur: (cur.execute(preencher(C["1.3"], receita)), cur.rowcount, consulta(
        cur, "SELECT id_receita, valor, dt_recebimento FROM T_SF_RECEITA WHERE descricao = 'Consultoria'")[1]))
    registrar("TC-C05", "receita válida", "1 linha; id 3; 750; 20/10/2025", f"{r[1]}; {r[2]}",
              r[1] == 1 and r[2] == [(3, Decimal("750"), "20/10/2025")])

    gasto = {"CÓDIGO DO USUÁRIO": 1, "CÓDIGO DA CONTA": 1, "CÓDIGO DA CATEGORIA": 6,
             "DESCRIÇÃO DO GASTO": "Show", "VALOR DO GASTO": "180.00", "DATA DO GASTO": "11/10/2025",
             "TIPO DO GASTO": "VARIAVEL", "CAMINHO DO COMPROVANTE": None}
    r = em_savepoint(con, lambda cur: (cur.execute(preencher(C["1.4"], gasto)), cur.rowcount, consulta(
        cur, "SELECT id_gasto, tipo, comprovante FROM T_SF_GASTO WHERE descricao = 'Show'")[1]))
    registrar("TC-C06", "gasto válido (comprovante nulo)", "1 linha; id 7; VARIAVEL; NULL", f"{r[1]}; {r[2]}",
              r[1] == 1 and r[2] == [(7, "VARIAVEL", None)])

    ok, msg = em_savepoint(con, lambda cur: espera_erro(
        cur, preencher(C["1.4"], {**gasto, "TIPO DO GASTO": "fixo"}), "ORA-02290", "CK_SF_GASTO_TIPO"))
    registrar("TC-C07", "gasto com tipo fora do domínio ('fixo')", "ORA-02290 CK_SF_GASTO_TIPO", msg, ok)

    ok, msg = em_savepoint(con, lambda cur: espera_erro(
        cur, preencher(C["1.4"], {**gasto, "CÓDIGO DA CONTA": 3}), "ORA-02291", "FK_SF_GASTO_CONTA"))
    registrar("TC-C07b", "gasto do usuário 1 na conta do usuário 2 (D-14)", "ORA-02291 FK_SF_GASTO_CONTA", msg, ok)

    invest = {"CÓDIGO DO USUÁRIO": 4, "CÓDIGO DA CONTA": 5, "NOME DO INVESTIMENTO": "Poupança Caixa",
              "TIPO DO INVESTIMENTO": "POUPANCA", "INSTITUIÇÃO": "Caixa", "VALOR APLICADO": "300.00",
              "TAXA DE RENTABILIDADE": "0.0617", "DATA DA APLICAÇÃO": "15/10/2025", "DATA DE VENCIMENTO": None}
    r = em_savepoint(con, lambda cur: (cur.execute(preencher(C["1.5"], invest)), cur.rowcount, consulta(
        cur, "SELECT id_investimento, status, tx_rentabilidade, dt_vencimento FROM T_SF_INVESTIMENTO "
             "WHERE nm_investimento = 'Poupança Caixa'")[1]))
    registrar("TC-C08", "investimento válido sem vencimento", "1 linha; id 6; ATIVO; 0.0617; NULL",
              f"{r[1]}; {r[2]}", r[1] == 1 and r[2] == [(6, "ATIVO", Decimal("0.0617"), None)])

    # ------------------------------------------------------------------ 2. Alteração
    log("\n## 2. Alteração")
    snap_usuarios = "SELECT id_usuario, nome, email, senha, avatar, dt_cadastro, ativo FROM T_SF_USUARIO ORDER BY 1"
    _, antes = consulta(cur, snap_usuarios)
    upd_u = {"CÓDIGO DO USUÁRIO": 4, "NOME DO USUÁRIO": "Diego Ramos Silva",
             "E-MAIL DO USUÁRIO": "diego.silva@exemplo.com", "CAMINHO DO AVATAR": "avatars/diego.png"}

    def tc_a01(cur):
        cur.execute(preencher(C["2.1"], upd_u))
        n = cur.rowcount
        _, depois = consulta(cur, snap_usuarios)
        return n, depois
    n, depois = em_savepoint(con, tc_a01)
    alterado = [d for a, d in zip(antes, depois) if a != d]
    ok = (n == 1 and len(alterado) == 1 and alterado[0][:3] == (4, "Diego Ramos Silva", "diego.silva@exemplo.com")
          and alterado[0][3] == antes[3][3] and alterado[0][5] == antes[3][5])
    registrar("TC-A01", "alterar usuário 4", "1 linha; só o usuário 4 muda; senha e dt_cadastro intactos",
              f"{n} linha; linhas alteradas: {[a[0] for a in alterado]}", ok)

    ok, msg = em_savepoint(con, lambda cur: espera_erro(
        cur, preencher(C["2.1"], {**upd_u, "E-MAIL DO USUÁRIO": "bruno@exemplo.com"}), "ORA-00001", "UK_SF_USUARIO_EMAIL"))
    registrar("TC-A02", "alterar e-mail para um já usado", "ORA-00001 UK_SF_USUARIO_EMAIL", msg, ok)

    upd_r = {"CÓDIGO DO USUÁRIO": 1, "CÓDIGO DA RECEITA": 2, "CÓDIGO DA CONTA": 1, "CÓDIGO DA CATEGORIA": 2,
             "DESCRIÇÃO DA RECEITA": "Freelance design (ajustado)", "VALOR DA RECEITA": "1350.00",
             "DATA DO RECEBIMENTO": "04/10/2025", "ORIGEM DA RECEITA": "FREELANCE",
             "RECORRÊNCIA DA RECEITA": "UNICA", "CAMINHO DO COMPROVANTE": "comprovantes/r2.pdf"}
    r = em_savepoint(con, lambda cur: (cur.execute(preencher(C["2.2"], upd_r)), cur.rowcount, consulta(
        cur, "SELECT valor, dt_recebimento FROM T_SF_RECEITA WHERE id_receita = 2")[1]))
    registrar("TC-A03", "alterar receita 2 do usuário 1", "1 linha; 1350; 04/10/2025", f"{r[1]}; {r[2]}",
              r[1] == 1 and r[2] == [(Decimal("1350"), "04/10/2025")])

    n = em_savepoint(con, lambda cur: (cur.execute(preencher(C["2.2"], {**upd_r, "CÓDIGO DO USUÁRIO": 2})), cur.rowcount)[1])
    registrar("TC-A04", "alterar receita 2 informando usuário 2", "0 linhas", f"{n} linhas", n == 0)

    upd_g = {"CÓDIGO DO USUÁRIO": 1, "CÓDIGO DO GASTO": 3, "CÓDIGO DA CONTA": 1, "CÓDIGO DA CATEGORIA": 4,
             "DESCRIÇÃO DO GASTO": "Padaria e café", "VALOR DO GASTO": "45.90", "DATA DO GASTO": "09/10/2025",
             "TIPO DO GASTO": "VARIAVEL", "CAMINHO DO COMPROVANTE": None}
    snap_gastos = "SELECT * FROM T_SF_GASTO ORDER BY id_gasto"
    _, g_antes = consulta(cur, snap_gastos)

    def tc_a05(cur):
        cur.execute(preencher(C["2.3"], upd_g))
        n = cur.rowcount
        return n, consulta(cur, snap_gastos)[1]
    n, g_depois = em_savepoint(con, tc_a05)
    mud = [d[0] for a, d in zip(g_antes, g_depois) if a != d]
    registrar("TC-A05", "alterar gasto 3 do usuário 1", "1 linha; só o gasto 3 muda", f"{n} linha; alterados {mud}",
              n == 1 and mud == [3])

    n = em_savepoint(con, lambda cur: (cur.execute(preencher(C["2.3"], {**upd_g, "CÓDIGO DO USUÁRIO": 2})), cur.rowcount)[1])
    registrar("TC-A06", "alterar gasto 3 informando usuário 2", "0 linhas", f"{n} linhas", n == 0)

    upd_i = {"CÓDIGO DO USUÁRIO": 1, "CÓDIGO DO INVESTIMENTO": 1, "CÓDIGO DA CONTA": 2,
             "NOME DO INVESTIMENTO": "CDB Nubank 100% CDI", "TIPO DO INVESTIMENTO": "CDB", "INSTITUIÇÃO": "Nubank",
             "VALOR APLICADO": "2000.00", "TAXA DE RENTABILIDADE": "0.1050", "DATA DA APLICAÇÃO": "01/08/2025",
             "DATA DE VENCIMENTO": "01/08/2027", "STATUS DO INVESTIMENTO": "RESGATADO"}
    r = em_savepoint(con, lambda cur: (cur.execute(preencher(C["2.4"], upd_i)), cur.rowcount, consulta(
        cur, "SELECT status FROM T_SF_INVESTIMENTO WHERE id_investimento = 1")[1]))
    registrar("TC-A07", "resgatar investimento 1 do usuário 1", "1 linha; RESGATADO", f"{r[1]}; {r[2]}",
              r[1] == 1 and r[2] == [("RESGATADO",)])

    # ------------------------------------------------------------------ 3. Consultas simples
    log("\n## 3. Consultas simples")
    cols, r = consulta(cur, preencher(C["3.1"], {"CÓDIGO DO USUÁRIO": 1}))
    registrar("TC-S01", "usuário 1 (sem senha)",
              "1 linha: 1, Larissa..., larissa@exemplo.com, NULL, 01/03/2025, S; sem coluna senha",
              f"{r}; colunas {cols}",
              r == [(1, "Larissa Gomes de Carvalho", "larissa@exemplo.com", None, "01/03/2025", "S")]
              and "senha" not in cols)

    _, r = consulta(cur, preencher(C["3.2"], {"CÓDIGO DO GASTO": 4, "CÓDIGO DO USUÁRIO": 1}))
    registrar("TC-S02", "gasto 4 do usuário 1", "(4, 1, 1, 4, Mercado extra, 412.30, 09/10/2025, VARIAVEL, NULL)",
              r, r == [(4, 1, 1, 4, "Mercado extra", Decimal("412.3"), "09/10/2025", "VARIAVEL", None)])

    _, r = consulta(cur, preencher(C["3.2"], {"CÓDIGO DO GASTO": 4, "CÓDIGO DO USUÁRIO": 2}))
    registrar("TC-S03", "gasto 4 informando usuário 2", "0 linhas", f"{len(r)} linhas", r == [])

    _, r = consulta(cur, preencher(C["3.3"], {"CÓDIGO DO INVESTIMENTO": 2, "CÓDIGO DO USUÁRIO": 1}))
    registrar("TC-S04a", "investimento 2 do usuário 1", "Tesouro Selic 2029, 1500, 0.1075, 15/09/2025, 01/03/2029, ATIVO",
              r, r == [(2, 1, 2, "Tesouro Selic 2029", "TESOURO", "Tesouro Nacional", Decimal("1500"),
                        Decimal("0.1075"), "15/09/2025", "01/03/2029", "ATIVO")])

    _, r = consulta(cur, preencher(C["3.3"], {"CÓDIGO DO INVESTIMENTO": 999, "CÓDIGO DO USUÁRIO": 1}))
    registrar("TC-S04b", "investimento 999", "0 linhas", f"{len(r)} linhas", r == [])

    # ------------------------------------------------------------------ 4. Ordenadas
    log("\n## 4. Consultas ordenadas")
    for caso, uid, esperado in [("TC-O01a", 1, [4, 3, 1, 2]), ("TC-O01b", 2, [6, 5]), ("TC-O01c", 3, [])]:
        _, r = consulta(cur, preencher(C["4.1"], {"CÓDIGO DO USUÁRIO": uid}))
        ids = [x[0] for x in r]
        donos = {x[1] for x in r}
        registrar(caso, f"despesas do usuário {uid}", esperado, ids, ids == esperado and donos <= {uid})
    for caso, uid, esperado in [("TC-O02a", 1, [3, 2, 1]), ("TC-O02b", 3, [5, 4]), ("TC-O02c", 2, [])]:
        _, r = consulta(cur, preencher(C["4.2"], {"CÓDIGO DO USUÁRIO": uid}))
        ids = [x[0] for x in r]
        donos = {x[1] for x in r}
        registrar(caso, f"investimentos do usuário {uid}", esperado, ids, ids == esperado and donos <= {uid})

    # ------------------------------------------------------------------ 5. Dashboard
    log("\n## 5. Dashboard")
    nulos5 = (None,) * 5
    casos = [
        ("TC-D01", 1, (4, "Mercado extra", Decimal("412.3"), "09/10/2025", "VARIAVEL"),
         (3, "FII HGLG11", "FII", Decimal("800"), "15/09/2025"), "usuário completo; empates resolvidos pelo maior ID"),
        ("TC-D03", 2, (6, "Cinema", Decimal("60"), "20/10/2025", "VARIAVEL"), nulos5, "sem investimentos"),
        ("TC-D04", 3, nulos5, (5, "Ações ITUB4", "ACOES", Decimal("1000"), "25/10/2025"), "sem gastos"),
        ("TC-D05", 4, nulos5, nulos5, "sem movimentação"),
    ]
    for caso, uid, g, i, desc in casos:
        cols, r = consulta(cur, preencher(C["5.1"], {"CÓDIGO DO USUÁRIO": uid}))
        ok = len(r) == 1 and r[0][0] == uid and tuple(r[0][4:9]) == g and tuple(r[0][9:14]) == i
        registrar(caso, f"dashboard usuário {uid} ({desc})", f"1 linha; gasto {g[0]}; investimento {i[0]}",
                  f"{len(r)} linha(s); gasto {r[0][4] if r else '-'}; investimento {r[0][9] if r else '-'}", ok)
        if uid == 1:
            registrar("TC-D02", "dashboard usuário 1 escolhe maior ID em empate de data",
                      "gasto 4 (não 3); investimento 3 (não 2)", f"gasto {r[0][4]}; investimento {r[0][9]}",
                      r[0][4] == 4 and r[0][9] == 3)
            registrar("TC-D06b", "isolamento: dados de outros usuários não vazam para o usuário 1",
                      "gasto != 6; investimento != 5", f"gasto {r[0][4]}; investimento {r[0][9]}",
                      r[0][4] != 6 and r[0][9] != 5)
            log(f"    colunas do dashboard: {cols}")
    _, r = consulta(cur, preencher(C["5.1"], {"CÓDIGO DO USUÁRIO": 999}))
    registrar("TC-D06", "dashboard usuário inexistente", "0 linhas", f"{len(r)} linhas", r == [])

    con.rollback()


def checar_estrutura(con):
    log("\n## Estrutura do schema")
    cur = con.cursor()
    _, r = consulta(cur, "SELECT COUNT(*) FROM user_tables WHERE table_name LIKE 'T\\_SF\\_%' ESCAPE '\\'")
    registrar("TC-E01", "tabelas T_SF_*", 10, r[0][0], r[0][0] == 10)
    _, r = consulta(cur, "SELECT object_type, object_name FROM user_objects WHERE status <> 'VALID'")
    registrar("TC-E02", "objetos inválidos", "0", len(r), r == [])
    _, r = consulta(cur, "SELECT constraint_name FROM user_constraints WHERE table_name LIKE 'T\\_SF\\_%' ESCAPE '\\' "
                         "AND constraint_name LIKE 'SYS\\_%' ESCAPE '\\' AND constraint_type <> 'C'")
    registrar("TC-E03", "constraints PK/FK/UK sem nome gerado pelo sistema", "0", len(r), r == [])
    fks_dicionario = sorted(re.findall(r"^\| `(FK_SF_\w+)`[^|]*\| FK \|",
                                       (RAIZ / "docs/05-banco-de-dados/dicionario-de-dados.md").read_text(encoding="utf-8"),
                                       re.M))
    _, r = consulta(cur, "SELECT constraint_name FROM user_constraints WHERE table_name LIKE 'T\\_SF\\_%' ESCAPE '\\' "
                         "AND constraint_type = 'R' ORDER BY 1")
    fks_banco = [x[0] for x in r]
    registrar("TC-E04", "FKs no banco = FKs do dicionário (mesmos nomes)", f"{len(fks_dicionario)} FKs",
              f"{len(fks_banco)} FKs; divergências: {sorted(set(fks_dicionario) ^ set(fks_banco)) or 'nenhuma'}",
              fks_banco == fks_dicionario)
    _, r = consulta(cur, "SELECT COUNT(*) FROM user_indexes WHERE index_name LIKE 'IX\\_SF\\_%' ESCAPE '\\'")
    registrar("TC-E05", "índices IX_SF_*", 11, r[0][0], r[0][0] == 11)
    _, r = consulta(cur, "SELECT COUNT(*) FROM user_tab_identity_cols WHERE table_name LIKE 'T\\_SF\\_%' ESCAPE '\\'")
    registrar("TC-E06", "colunas IDENTITY", 10, r[0][0], r[0][0] == 10)
    _, r = consulta(cur, "SELECT banner_full FROM v$version")
    log(f"    versão: {r[0][0]}")


def relatorio(titulo_execucao: str):
    EVID.mkdir(parents=True, exist_ok=True)
    hoje = dt.date.today().isoformat()
    total, ok = len(RESULTADOS), sum(r.passou for r in RESULTADOS)
    linhas = [
        "# Relatório de testes — comandos SQL Fintech (T13)", "",
        f"| Item | Valor |", "|---|---|",
        f"| Data | {dt.datetime.now():%Y-%m-%d %H:%M} |",
        f"| Execução | {titulo_execucao} |",
        f"| Resultado | **{ok}/{total} passaram** |", "",
        "Gerado por `database/testes/executar_testes.py`. Cada comando testado é o comando do entregável "
        "(`database/comandos/fintech-comandos.sql`) com as máscaras substituídas por valores — sem reescrita.", "",
        "| Caso | Descrição | Esperado | Obtido | Resultado |", "|---|---|---|---|---|",
    ]
    for r in RESULTADOS:
        esc = lambda s: s.replace("|", "\\|")
        linhas.append(f"| {r.caso} | {esc(r.descricao)} | {esc(r.esperado)} | {esc(r.obtido)} | "
                      f"{'✅ Passou' if r.passou else '❌ Falhou'} |")
    (EVID / "relatorio-testes.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    (EVID / f"execucao-{hoje}.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    log(f"\nRESULTADO: {ok}/{total} passaram")
    return ok == total


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    con = conectar()
    log(f"# Execução {dt.datetime.now():%Y-%m-%d %H:%M:%S} — modo {modo}")
    if modo in ("setup", "tudo"):
        setup(con)
    if modo in ("testes", "tudo"):
        checar_estrutura(con)
        suite(con)
        import testes_constraints  # noqa: E402  (mesmo diretório)
        testes_constraints.main()
        sucesso = relatorio(modo)
        sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
