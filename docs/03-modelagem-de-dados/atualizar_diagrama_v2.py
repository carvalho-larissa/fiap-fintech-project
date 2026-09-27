"""
Atualiza o diagrama relacional da Fase 3 para a v2 (Fase 4).

Entrada/saída: docs/03-modelagem-de-dados/modelo-relacional.drawio (editado in-place;
o original da Fase 3 continua preservado dentro de modelagem-de-dados.pdf).

Mudanças (ver docs/05-banco-de-dados/dicionario-de-dados.md):
  1. Desloca o diagrama 200px para baixo para abrir espaço no topo.
  2. Adiciona T_SF_INVESTIMENTO (D-01) nas páginas lógica e física, clonando o estilo de T_SF_GASTO.
  3. Relacionamentos T_SF_USUARIO 1:N e T_SF_CONTA_BANCARIA 1:N com T_SF_INVESTIMENTO.
  4. Remove a obrigatoriedade (*) de T_SF_PARCELA.dt_pagamento (D-15).
  5. Renomeia as legendas de PK/FK da página física para a convenção v2 (FKs únicas, FK composta D-14).
  6. Atualiza os títulos para indicar a versão.

Idempotência: aborta se T_SF_INVESTIMENTO já existir no arquivo.
Uso: uv run python docs/03-modelagem-de-dados/atualizar_diagrama_v2.py
"""
import copy
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ARQ = Path(__file__).with_name("modelo-relacional.drawio")
SHIFT_Y = 200
INV_X, INV_Y = 420, 20
COLS = (50, 140, 120)  # larguras das colunas: chave | nome | tipo
ROW_H = 26

# (chave, coluna, tipo lógico, tipo físico, obrigatória)
INVEST_COLS = [
    ("PK", "id_investimento", "NUMERIC(10)", "NUMBER(10)", True),
    ("FK", "id_usuario", "NUMERIC(10)", "NUMBER(10)", True),
    ("FK", "id_conta", "NUMERIC(10)", "NUMBER(10)", True),
    ("", "nm_investimento", "VARCHAR(150)", "VARCHAR2(150)", True),
    ("", "tipo", "VARCHAR(30)", "VARCHAR2(30)", True),
    ("", "instituicao", "VARCHAR(100)", "VARCHAR2(100)", False),
    ("", "vl_aplicado", "NUMERIC(15,2)", "NUMBER(15,2)", True),
    ("", "tx_rentabilidade", "NUMERIC(7,4)", "NUMBER(7,4)", False),
    ("", "dt_aplicacao", "Date", "DATE", True),
    ("", "dt_vencimento", "Date", "DATE", False),
    ("", "status", "VARCHAR(15)", "VARCHAR2(15)", True),
]
INVEST_LEGENDAS = [
    "🔑 PK_T_SF_INVESTIMENTO (id_investimento)",
    "🔗 FK_SF_INVEST_USUARIO (id_usuario)",
    "🔗 FK_SF_INVEST_CONTA (id_conta, id_usuario)",
]

# Legendas da página física: (tabela, texto antigo) -> texto novo
LEGENDAS_V2 = {
    ("T_SF_GASTO", "FK_T_SF_USUARIO"): "🔗 FK_SF_GASTO_USUARIO (id_usuario)",
    ("T_SF_GASTO", "FK_T_SF_CONTA_BANCARIA"): "🔗 FK_SF_GASTO_CONTA (id_conta, id_usuario)",
    ("T_SF_GASTO", "FK_T_SF_CATEGORIA"): "🔗 FK_SF_GASTO_CATEGORIA (id_categoria)",
    ("T_SF_RECEITA", "FK_T_SF_USUARIO"): "🔗 FK_SF_RECEITA_USUARIO (id_usuario)",
    ("T_SF_RECEITA", "FK_T_SF_CONTA_BANCARIA"): "🔗 FK_SF_RECEITA_CONTA (id_conta, id_usuario)",
    ("T_SF_RECEITA", "FK_T_SF_CATEGORIA"): "🔗 FK_SF_RECEITA_CATEGORIA (id_categoria)",
    ("T_SF_CONTA_BANCARIA", "FK_T_SF_USUARIO"): "🔗 FK_SF_CONTA_USUARIO (id_usuario)",
    ("T_SF_DIVIDA", "FK_T_SF_USUARIO"): "🔗 FK_SF_DIVIDA_USUARIO (id_usuario)",
    ("T_SF_META", "FK_T_SF_USUARIO"): "🔗 FK_SF_META_USUARIO (id_usuario)",
    ("T_SF_PARCELA", "FK_T_SF_DIVIDA"): "🔗 FK_SF_PARCELA_DIVIDA (id_divida)",
    ("T_SF_APORTE_META", "FK_T_SF_META"): "🔗 FK_SF_APORTE_META (id_meta)",
}


def geo(c):
    return c.find("mxGeometry")


def fnum(v, default=0.0):
    return float(v) if v is not None else default


def fmt(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def processar(diagram, fisico: bool, prefixo: str):
    model = diagram.find("mxGraphModel")
    root = model.find("root")
    cells = list(root)
    byid = {c.get("id"): c for c in cells}
    layer = cells[1].get("id")

    def tabela_de(c):
        while c is not None and "shape=table;" not in (c.get("style") or ""):
            c = byid.get(c.get("parent"))
        return c

    tabelas = {c.get("value"): c for c in cells if "shape=table;" in (c.get("style") or "")}
    if "T_SF_INVESTIMENTO" in tabelas:
        sys.exit("T_SF_INVESTIMENTO já existe no diagrama — nada a fazer.")

    # --- 4. D-15: remove o asterisco de dt_pagamento (antes do deslocamento) ---
    parc = tabelas["T_SF_PARCELA"]
    px, py = fnum(geo(parc).get("x")), fnum(geo(parc).get("y"))
    linha_pag = 5  # id_parcela, id_divida, nr_parcela, vl_parcela, dt_vencimento, dt_pagamento
    y_min = py + 30 + linha_pag * ROW_H
    removidos = 0
    for c in list(root):
        if c.get("value") == "*" and c.get("parent") == layer:
            g = geo(c)
            x, y = fnum(g.get("x")), fnum(g.get("y"))
            if px <= x <= px + 60 and y_min - 2 <= y <= y_min + ROW_H - 2:
                root.remove(c)
                removidos += 1
    assert removidos == 1, f"esperava remover 1 asterisco de dt_pagamento, removi {removidos}"

    # --- 5. Legendas v2 (página física) ---
    if fisico:
        for c in root:
            v = c.get("value") or ""
            if c.get("parent") != layer or not (v.startswith("🔑") or v.startswith("🔗")):
                continue
            g = geo(c)
            x, y = fnum(g.get("x")), fnum(g.get("y"))
            dono = None
            for nome, t in tabelas.items():
                tg = geo(t)
                tx, ty = fnum(tg.get("x")), fnum(tg.get("y"))
                if tx - 10 <= x <= tx + fnum(tg.get("width")) and ty <= y <= ty + fnum(tg.get("height")):
                    dono = (nome, t)
            assert dono, f"legenda sem tabela: {v}"
            nome, t = dono
            if v.startswith("🔗"):
                chave = v.split()[1]
                novo = LEGENDAS_V2.get((nome, chave))
                assert novo, f"sem mapeamento para {(nome, chave)}"
                c.set("value", novo)
            tg = geo(t)
            g.set("width", fmt(fnum(tg.get("x")) + fnum(tg.get("width")) - x - 4))
            c.set("style", c.get("style").rstrip(";") + ";fontSize=11;")

    # --- 6. Títulos ---
    for c in root:
        if c.get("value") in ("Modelo Lógico", "Modelo Físico"):
            c.set("value", c.get("value") + "<br><font style=\"font-size: 14px;\">v2 · Fase 4</font>")

    # --- 1. Deslocamento vertical ---
    for c in root:
        if c.get("parent") != layer:
            continue
        g = geo(c)
        if g is None:
            continue
        if c.get("value") in ("Modelo Lógico<br><font style=\"font-size: 14px;\">v2 · Fase 4</font>",
                              "Modelo Físico<br><font style=\"font-size: 14px;\">v2 · Fase 4</font>",
                              "Sistema Fintech (SF)"):
            continue
        if c.get("edge") == "1":
            for p in g.iter("mxPoint"):
                if p.get("as") != "offset" and p.get("y") is not None:
                    p.set("y", fmt(fnum(p.get("y")) + SHIFT_Y))
        elif g.get("y") is not None or c.get("vertex") == "1":
            g.set("y", fmt(fnum(g.get("y")) + SHIFT_Y))
    model.set("pageHeight", str(int(model.get("pageHeight")) + SHIFT_Y))

    # --- 2. Nova tabela, clonando o estilo de T_SF_GASTO ---
    gasto = tabelas["T_SF_GASTO"]
    filhos = {}
    for c in root:
        filhos.setdefault(c.get("parent"), []).append(c)
    linhas_gasto = sorted(filhos[gasto.get("id")], key=lambda r: fnum(geo(r).get("y")))
    modelo_chave, modelo_comum = linhas_gasto[0], linhas_gasto[4]
    modelos_legenda = linhas_gasto[9:] if fisico else []

    seq = iter(range(1, 10_000))
    nid = lambda: f"{prefixo}-{next(seq)}"
    largura = sum(COLS)

    tab = copy.deepcopy(gasto)
    tab.set("id", nid())
    tab.set("value", "T_SF_INVESTIMENTO")
    tg = geo(tab)
    tg.set("x", str(INV_X))
    tg.set("y", str(INV_Y))
    tg.set("width", str(largura))
    novos = [tab]

    def nova_linha(modelo, y, h, textos):
        r = copy.deepcopy(modelo)
        r.set("id", nid())
        r.set("parent", tab.get("id"))
        rg = geo(r)
        rg.set("y", str(y))
        rg.set("height", str(h))
        rg.set("width", str(largura))
        novos.append(r)
        x = 0
        for (mc, largura_col, texto) in zip(filhos[modelo.get("id")], COLS, textos):
            k = copy.deepcopy(mc)
            k.set("id", nid())
            k.set("parent", r.get("id"))
            kg = geo(k)
            if x:
                kg.set("x", str(x))
            kg.set("width", str(largura_col))
            kg.set("height", str(h))
            ag = kg.find("mxRectangle")
            if ag is not None:
                ag.set("width", str(largura_col))
                ag.set("height", str(h))
            if texto is None:
                k.attrib.pop("value", None)
            else:
                k.set("value", texto)
            novos.append(k)
            x += largura_col

    y = 30
    asteriscos = []
    for chave, col, tlog, tfis, nn in INVEST_COLS:
        modelo = modelo_chave if chave else modelo_comum
        nome = col if chave else "   " + col
        nova_linha(modelo, y, ROW_H, (chave or None, nome, tfis if fisico else tlog))
        if nn:
            asteriscos.append(INV_Y + y + 5)
        y += ROW_H

    legendas_pos = []
    if fisico:
        nova_linha(modelos_legenda[0], y, ROW_H, (None, None, None))
        legendas_pos.append(INV_Y + y)
        y += ROW_H
        h = ROW_H * (len(INVEST_LEGENDAS) - 1)
        nova_linha(modelos_legenda[1], y, h, (None, None, None))
        legendas_pos += [INV_Y + y + ROW_H * i for i in range(len(INVEST_LEGENDAS) - 1)]
        y += h
    tg.set("height", str(y))

    # asteriscos vermelhos (mesmo estilo dos existentes)
    ast_modelo = next(c for c in root if c.get("value") == "*")
    for ay in asteriscos:
        a = copy.deepcopy(ast_modelo)
        a.set("id", nid())
        ag = geo(a)
        ag.set("x", str(INV_X + 20))
        ag.set("y", str(ay))
        ag.set("width", "20")
        ag.set("height", "20")
        novos.append(a)

    # legendas PK/FK
    if fisico:
        leg_modelo = next(c for c in root if (c.get("value") or "").startswith("🔑"))
        for texto, ly in zip(INVEST_LEGENDAS, legendas_pos):
            l = copy.deepcopy(leg_modelo)
            l.set("id", nid())
            l.set("value", texto)
            lg = geo(l)
            lg.set("x", str(INV_X + 4))
            lg.set("y", str(ly))
            lg.set("width", str(largura - 8))
            lg.set("height", str(ROW_H))
            novos.append(l)

    # --- 3. Relacionamentos ---
    usuario = tabelas["T_SF_USUARIO"]
    conta = tabelas["T_SF_CONTA_BANCARIA"]
    ug, cg = geo(usuario), geo(conta)
    ux, uy, uw = fnum(ug.get("x")), fnum(ug.get("y")), fnum(ug.get("width"))
    cx, cy, ch = fnum(cg.get("x")), fnum(cg.get("y")), fnum(cg.get("height"))
    altura = y

    base_solida = ("edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=light-dark(#B3B3B3,#B3B3B3);"
                   "strokeWidth=1;endArrow=ERzeroToMany;startArrow=ERmandOne;fontSize=13;endFill=0;startFill=0;")
    base_tracejada = ("edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=light-dark(#B3B3B3,#B3B3B3);"
                      "strokeWidth=1;endArrow=ERzeroToMany;startArrow=ERzeroToOne;fontSize=13;endFill=0;"
                      "startFill=0;dashed=1;dashPattern=8 8;")

    def aresta(estilo, origem, destino, pontos):
        e = ET.Element("mxCell", {"id": nid(), "style": estilo, "edge": "1", "parent": layer,
                                  "source": origem.get("id"), "target": destino.get("id")})
        g = ET.SubElement(e, "mxGeometry", {"relative": "1", "as": "geometry"})
        arr = ET.SubElement(g, "Array", {"as": "points"})
        for (px_, py_) in pontos:
            ET.SubElement(arr, "mxPoint", {"x": fmt(px_), "y": fmt(py_)})
        novos.append(e)

    # USUARIO (topo, 10% da largura) -> sobe pelo corredor entre RECEITA e DIVIDA -> lado direito do INVESTIMENTO
    sai_x = ux + uw * 0.1
    entra_y = INV_Y + altura * 0.55
    aresta(base_solida + f"exitX=0.1;exitY=0;exitDx=0;exitDy=0;exitPerimeter=0;"
                         f"entryX=1;entryY=0.55;entryDx=0;entryDy=0;entryPerimeter=0;",
           usuario, tab, [(sai_x, entra_y)])
    # CONTA (lado esquerdo) -> corredor x=450 entre GASTO e RECEITA -> base do INVESTIMENTO
    sai_y = cy + ch * 0.3
    corredor_x = INV_X + 30
    aresta(base_tracejada + f"exitX=0;exitY=0.3;exitDx=0;exitDy=0;exitPerimeter=0;"
                            f"entryX={30 / largura:.3f};entryY=1;entryDx=0;entryDy=0;entryPerimeter=0;",
           conta, tab, [(corredor_x, sai_y)])

    for c in novos:
        root.append(c)
    return len(novos)


def main():
    tree = ET.parse(ARQ)
    diagramas = list(tree.getroot().iter("diagram"))
    assert [d.get("name") for d in diagramas] == ["Modelo Lógico", "Modelo Físico"]
    n1 = processar(diagramas[0], fisico=False, prefixo="v2-log")
    n2 = processar(diagramas[1], fisico=True, prefixo="v2-fis")
    ET.indent(tree, space="  ")
    tree.write(ARQ, encoding="utf-8", xml_declaration=False)
    print(f"OK: {n1} células na página lógica, {n2} na física -> {ARQ}")


if __name__ == "__main__":
    main()
