"""
Verificação estática (sem banco) dos artefatos SQL da Fase 6.

Não substitui a execução em Oracle (T13) — pega erros de contrato cedo:
  1. DDL x dicionário de dados x diagrama (.drawio, página física): mesmas tabelas,
     colunas, tipos e obrigatoriedade.
  2. Nomes de identificadores <= 30 caracteres (compatibilidade Oracle).
  3. Comandos x DDL:
     - toda coluna referenciada existe na tabela;
     - máscara de TEXTO entre aspas, NUMÉRICA sem aspas, DATA com TO_DATE (RNF-03, D-03);
     - INSERT sem coluna de ID e com todas as colunas NOT NULL sem default (D-02);
     - UPDATE nunca altera PK, id_usuario, senha, dt_cadastro/dt_criacao (D-06) e
       filtra pela PK (+ id_usuario nas tabelas de lançamento) (RNF-05);
     - nenhum SELECT * e nenhuma consulta retorna senha (D-05);
     - consultas ordenadas com desempate por ID (D-08);
     - nenhum COMMIT no entregável (D-07);
     - 15 comandos, na ordem e quantidade do enunciado.
  4. Sintaxe: parse de cada comando com sqlglot (dialeto Oracle), com máscaras substituídas.

Uso: uv run --with sqlglot python database/testes/verificar_estatico.py
Saída: relatório no terminal; código de saída 1 se houver falha.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DDL = RAIZ / "database/ddl/01-create-tables.sql"
DICIONARIO = RAIZ / "docs/05-banco-de-dados/dicionario-de-dados.md"
COMANDOS = RAIZ / "database/comandos/fintech-comandos.sql"
SEED = RAIZ / "database/dml/02-seed.sql"

falhas: list[str] = []
oks = 0


def check(cond: bool, msg: str):
    global oks
    if cond:
        oks += 1
    else:
        falhas.append(msg)


def sem_comentarios(sql: str) -> str:
    return re.sub(r"--[^\n]*", "", sql)


def split_topo(s: str, sep: str = ",") -> list[str]:
    """Divide por `sep` ignorando parênteses e literais."""
    partes, nivel, atual, aspas = [], 0, [], False
    for ch in s:
        if ch == "'":
            aspas = not aspas
        elif not aspas and ch == "(":
            nivel += 1
        elif not aspas and ch == ")":
            nivel -= 1
        if ch == sep and nivel == 0 and not aspas:
            partes.append("".join(atual).strip())
            atual = []
        else:
            atual.append(ch)
    if "".join(atual).strip():
        partes.append("".join(atual).strip())
    return partes


# ---------------------------------------------------------------------------
# 1. Modelo a partir do DDL
# ---------------------------------------------------------------------------
def ler_ddl():
    sql = sem_comentarios(DDL.read_text(encoding="utf-8"))
    tabelas = {}
    for m in re.finditer(r"CREATE TABLE (\w+)\s*\((.*?)\n\);", sql, re.S):
        nome, corpo = m.group(1), m.group(2)
        cols, constraints = {}, []
        for item in split_topo(corpo):
            item = " ".join(item.split())
            if item.upper().startswith("CONSTRAINT"):
                constraints.append(item)
                continue
            partes = item.split(" ", 2)
            col, tipo, resto = partes[0], partes[1], (partes[2] if len(partes) > 2 else "")
            cols[col] = {
                "tipo": tipo.upper(),
                "nn": "NOT NULL" in resto.upper() or "IDENTITY" in resto.upper(),
                "default": "DEFAULT" in resto.upper(),
                "identity": "IDENTITY" in resto.upper(),
            }
        tabelas[nome] = {"cols": cols, "constraints": constraints}
    nomes = re.findall(r"CONSTRAINT (\w+)", sql) + re.findall(r"CREATE INDEX (\w+)", sql)
    return tabelas, nomes


def ler_dicionario():
    md = DICIONARIO.read_text(encoding="utf-8")
    tabelas = {}
    for bloco in re.split(r"\n### 3\.\d+ ", md)[1:]:
        nome = re.match(r"`(\w+)`", bloco).group(1)
        cols = {}
        for linha in bloco.splitlines():
            m = re.match(r"\| `(\w+)`[^|]*\| `([^`]+)` \|\s*(✔?)\s*\|", linha)
            if m:
                cols[m.group(1)] = {"tipo": m.group(2).upper(), "nn": m.group(3) == "✔"}
        tabelas[nome] = cols
    return tabelas


ddl, nomes_objetos = ler_ddl()
dic = ler_dicionario()

check(len(ddl) == 10, f"DDL deveria ter 10 tabelas, tem {len(ddl)}")
check(set(ddl) == set(dic), f"Tabelas divergentes DDL x dicionário: {set(ddl) ^ set(dic)}")
for t in ddl:
    for c, meta in dic.get(t, {}).items():
        d = ddl[t]["cols"].get(c)
        check(d is not None, f"{t}.{c} está no dicionário mas não no DDL")
        if d:
            check(d["tipo"] == meta["tipo"], f"{t}.{c}: tipo DDL {d['tipo']} != dicionário {meta['tipo']}")
            check(d["nn"] == meta["nn"], f"{t}.{c}: NOT NULL DDL {d['nn']} != dicionário {meta['nn']}")
    extras = set(ddl[t]["cols"]) - set(dic.get(t, {}))
    check(not extras, f"{t}: colunas no DDL fora do dicionário: {extras}")

for n in nomes_objetos + list(ddl):
    check(len(n) <= 30, f"Identificador com mais de 30 caracteres: {n} ({len(n)})")
check(len(nomes_objetos) == len(set(nomes_objetos)), "Nomes de constraint/índice duplicados")


# ---------------------------------------------------------------------------
# 1b. Diagrama (.drawio, página física) x DDL: mesmas tabelas, colunas, tipos e
#     obrigatoriedade (asterisco vermelho alinhado à linha da coluna)
# ---------------------------------------------------------------------------
def ler_diagrama_fisico():
    import xml.etree.ElementTree as ET

    raiz = ET.parse(RAIZ / "docs/03-modelagem-de-dados/modelo-relacional.drawio").getroot()
    pagina = [d for d in raiz.iter("diagram") if d.get("name") == "Modelo Físico"][0]
    cells = list(pagina.iter("mxCell"))
    filhos: dict[str, list] = {}
    for c in cells:
        filhos.setdefault(c.get("parent"), []).append(c)
    geo = lambda c: c.find("mxGeometry")
    num = lambda v: float(v) if v is not None else 0.0
    asteriscos = [(num(geo(c).get("x")), num(geo(c).get("y"))) for c in cells if c.get("value") == "*"]
    modelo = {}
    for t in cells:
        if "shape=table;" not in (t.get("style") or ""):
            continue
        tx, ty = num(geo(t).get("x")), num(geo(t).get("y"))
        cols = {}
        for linha in filhos.get(t.get("id"), []):
            celulas = filhos.get(linha.get("id"), [])
            if len(celulas) != 3 or not (celulas[1].get("value") or "").strip():
                continue  # linhas de legenda PK/FK
            nome = (celulas[1].get("value") or "").replace("\xa0", " ").strip()
            tipo = (celulas[2].get("value") or "").strip().upper()
            ly = ty + num(geo(linha).get("y"))
            lh = num(geo(linha).get("height"))
            nn = any(tx <= ax <= tx + 70 and ly - 6 <= ay <= ly + lh - 6 for ax, ay in asteriscos)
            cols[nome] = {"tipo": tipo, "nn": nn}
        modelo[t.get("value")] = cols
    return modelo


diag = ler_diagrama_fisico()
check(set(diag) == set(ddl), f"Tabelas divergentes diagrama x DDL: {set(diag) ^ set(ddl)}")
for t in ddl:
    dcols, tcols = diag.get(t, {}), ddl[t]["cols"]
    check(set(dcols) == set(tcols), f"{t}: colunas divergentes diagrama x DDL: {set(dcols) ^ set(tcols)}")
    for c in set(dcols) & set(tcols):
        check(dcols[c]["tipo"] == tcols[c]["tipo"],
              f"{t}.{c}: tipo diagrama {dcols[c]['tipo']} != DDL {tcols[c]['tipo']}")
        check(dcols[c]["nn"] == tcols[c]["nn"],
              f"{t}.{c}: obrigatoriedade diagrama {dcols[c]['nn']} != DDL {tcols[c]['nn']}")

PK = {t: next(c for c, m in v["cols"].items() if m["identity"]) for t, v in ddl.items()}


# ---------------------------------------------------------------------------
# 2. Comandos
# ---------------------------------------------------------------------------
def classificar_valor(v: str) -> str:
    v = v.strip()
    if re.fullmatch(r"'\[[^\]]+\]'", v):
        return "texto_mascara"
    if re.fullmatch(r"\[[^\]]+\]", v):
        return "numero_mascara"
    if re.fullmatch(r"TO_DATE\('\[[^\]]+\]', 'DD/MM/YYYY'\)", v):
        return "data_mascara"
    if v.upper() == "SYSDATE":
        return "sysdate"
    if re.fullmatch(r"'[^']*'", v):
        return "texto_literal"
    return "outro"


def tipo_base(tipo: str) -> str:
    if tipo.startswith(("VARCHAR2", "CHAR")):
        return "texto"
    if tipo.startswith("NUMBER"):
        return "numero"
    if tipo.startswith("DATE"):
        return "data"
    return "?"


COMPATIVEL = {
    "texto": {"texto_mascara", "texto_literal"},
    "numero": {"numero_mascara"},
    "data": {"data_mascara", "sysdate"},
}


def checar_valor(tabela, col, valor, ctx):
    tb = tipo_base(ddl[tabela]["cols"][col]["tipo"])
    cls = classificar_valor(valor)
    check(cls in COMPATIVEL[tb], f"{ctx}: {tabela}.{col} ({tb}) recebeu valor '{valor}' ({cls})")


texto = COMANDOS.read_text(encoding="utf-8")
itens = re.findall(r"^-- (\d\.\d) (.+)$", texto, re.M)
esperado = ["1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4",
            "3.1", "3.2", "3.3", "4.1", "4.2", "5.1"]
check([i for i, _ in itens] == esperado, f"Itens do entregável fora da ordem/quantidade: {[i for i, _ in itens]}")

stmts = [s.strip() for s in sem_comentarios(texto).split(";") if s.strip()]
check(len(stmts) == 15, f"Entregável deveria ter 15 comandos, tem {len(stmts)}")
check("COMMIT" not in sem_comentarios(texto).upper(), "Entregável contém COMMIT (D-07)")

PROIBIDAS_SET = {"id_usuario", "senha", "dt_cadastro", "dt_criacao"}
LANCAMENTOS = {"T_SF_RECEITA", "T_SF_GASTO", "T_SF_INVESTIMENTO"}

for (item, titulo), s in zip(itens, stmts):
    ctx = f"[{item}]"
    s1 = " ".join(s.split())
    up = s1.upper()
    if up.startswith("INSERT"):
        m = re.match(r"INSERT INTO (\w+) \((.*?)\) VALUES \((.*)\)$", s1, re.I)
        check(m is not None, f"{ctx} INSERT fora do formato esperado")
        if not m:
            continue
        t, cols, vals = m.group(1), split_topo(m.group(2)), split_topo(m.group(3))
        check(t in ddl, f"{ctx} tabela inexistente {t}")
        check(len(cols) == len(vals), f"{ctx} {len(cols)} colunas x {len(vals)} valores")
        check(PK[t] not in cols, f"{ctx} INSERT informa a PK {PK[t]} (D-02)")
        for c, v in zip(cols, vals):
            check(c in ddl[t]["cols"], f"{ctx} coluna inexistente {t}.{c}")
            if c in ddl[t]["cols"]:
                checar_valor(t, c, v, ctx)
        obrig = {c for c, mt in ddl[t]["cols"].items() if mt["nn"] and not mt["default"] and not mt["identity"]}
        check(obrig <= set(cols), f"{ctx} faltam colunas obrigatórias: {obrig - set(cols)}")
    elif up.startswith("UPDATE"):
        m = re.match(r"UPDATE (\w+) SET (.*) WHERE (.*)$", s1, re.I)
        check(m is not None, f"{ctx} UPDATE sem WHERE")
        if not m:
            continue
        t, sets, where = m.group(1), split_topo(m.group(2)), m.group(3)
        for a in sets:
            c, v = [x.strip() for x in a.split("=", 1)]
            check(c in ddl[t]["cols"], f"{ctx} coluna inexistente {t}.{c}")
            check(c != PK[t] and c not in PROIBIDAS_SET, f"{ctx} coluna proibida no SET: {c} (D-06)")
            if c in ddl[t]["cols"]:
                checar_valor(t, c, v, ctx)
        check(re.search(rf"\b{PK[t]} = \[", where) is not None, f"{ctx} WHERE sem a PK {PK[t]}")
        if t in LANCAMENTOS:
            check(re.search(r"\bid_usuario = \[", where) is not None, f"{ctx} WHERE sem id_usuario (RNF-05)")
    elif up.startswith("SELECT"):
        check(not re.search(r"SELECT \*|\.\*", s1, re.I), f"{ctx} usa SELECT *")
        check(not re.search(r"\bsenha\b", s1, re.I), f"{ctx} retorna senha (D-05)")
        check("[CÓDIGO DO USUÁRIO]" in s1, f"{ctx} não filtra pelo código do usuário")
        m = re.match(r"SELECT (.*?) FROM (\w+) WHERE", s1, re.I)
        if m and item != "5.1":
            t = m.group(2)
            for c in split_topo(m.group(1)):
                check(c in ddl[t]["cols"], f"{ctx} coluna inexistente {t}.{c}")
        if item.startswith("4."):
            check(re.search(r"ORDER BY \w+ DESC, id_\w+ DESC$", s1) is not None,
                  f"{ctx} ordenação sem desempate data DESC, id DESC (D-08)")
        if item == "5.1":
            check(up.count("LEFT JOIN") == 2, f"{ctx} dashboard deveria ter 2 LEFT JOIN (D-12)")
            check(up.count("ROW_NUMBER()") == 2 and up.count("RN = 1") == 2,
                  f"{ctx} dashboard deveria selecionar 1 registro de cada lado")
            for t in ("T_SF_GASTO", "T_SF_INVESTIMENTO"):
                sub = re.search(rf"\(SELECT ((?:(?!\(SELECT).)*?) FROM {t}\b", s1).group(1)
                for c in split_topo(sub):
                    if not c.upper().startswith("ROW_NUMBER"):
                        check(c in ddl[t]["cols"], f"{ctx} coluna inexistente {t}.{c}")
    else:
        check(False, f"{ctx} comando não reconhecido")

# ---------------------------------------------------------------------------
# 3. Sintaxe (sqlglot, dialeto Oracle)
# ---------------------------------------------------------------------------
try:
    import sqlglot
    from sqlglot.errors import ParseError

    def exemplificar(s: str) -> str:
        s = re.sub(r"TO_DATE\('\[[^\]]+\]'", "TO_DATE('01/01/2025'", s)
        s = re.sub(r"'\[[^\]]+\]'", "'X'", s)
        return re.sub(r"\[[^\]]+\]", "1", s)

    for (item, _), s in zip(itens, stmts):
        try:
            sqlglot.parse_one(exemplificar(s), read="oracle")
            check(True, "")
        except ParseError as e:
            check(False, f"[{item}] erro de sintaxe (sqlglot): {str(e).splitlines()[0]}")
    for s in [x for x in sem_comentarios(SEED.read_text(encoding="utf-8")).split(";") if x.strip()]:
        if s.strip().upper().startswith("INSERT"):
            try:
                sqlglot.parse_one(s, read="oracle")
                check(True, "")
            except ParseError as e:
                check(False, f"[seed] erro de sintaxe: {str(e).splitlines()[0]}")
    sintaxe = "sqlglot OK"
except ImportError:
    sintaxe = "sqlglot não instalado — checagem de sintaxe pulada"

# ---------------------------------------------------------------------------
print(f"Verificações OK: {oks} · Falhas: {len(falhas)} · {sintaxe}")
for f in falhas:
    print("  FALHA", f)
sys.exit(1 if falhas else 0)
