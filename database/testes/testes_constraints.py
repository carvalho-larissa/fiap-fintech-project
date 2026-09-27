"""Testes negativos de constraints do DDL (T06) e revisão de sintaxe 19c (D-16)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import executar_testes as t  # noqa: E402

if __name__ != "__main__":
    # importado pelo executar_testes: reusar o MESMO módulo já carregado (__main__),
    # para que os resultados entrem no mesmo relatório
    t = sys.modules["__main__"]

CASOS = [
    ("TC-K01", "valor de gasto negativo", "ORA-02290", "CK_SF_GASTO_VALOR",
     "INSERT INTO T_SF_GASTO (id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto) "
     "VALUES (1, 1, 4, 'x', -1, SYSDATE)"),
    ("TC-K02", "parcela PAGA sem data de pagamento (D-15)", "ORA-02290", "CK_SF_PARCELA_PAGAMENTO",
     "INSERT INTO T_SF_PARCELA (id_divida, nr_parcela, vl_parcela, dt_vencimento, status) "
     "VALUES (1, 3, 246.66, SYSDATE, 'PAGA')"),
    ("TC-K03", "parcela PENDENTE sem data de pagamento é aceita (D-15)", None, None,
     "INSERT INTO T_SF_PARCELA (id_divida, nr_parcela, vl_parcela, dt_vencimento, status) "
     "VALUES (1, 3, 246.66, SYSDATE, 'PENDENTE')"),
    ("TC-K04", "vencimento anterior à aplicação", "ORA-02290", "CK_SF_INVEST_DT_VENCIMENTO",
     "INSERT INTO T_SF_INVESTIMENTO (id_usuario, id_conta, nm_investimento, tipo, vl_aplicado, dt_aplicacao, dt_vencimento) "
     "VALUES (1, 2, 'x', 'CDB', 10, DATE '2025-10-10', DATE '2025-01-01')"),
    ("TC-K05", "e-mail sem formato válido", "ORA-02290", "CK_SF_USUARIO_EMAIL",
     "INSERT INTO T_SF_USUARIO (nome, email, senha) VALUES ('x', 'sem-arroba', 'h')"),
    ("TC-K06", "taxa de juros de cartão 12,99% a.m. cabe em NUMBER(5,4) como fração (D-17)", None, None,
     "UPDATE T_SF_DIVIDA SET tx_juros_mensal = 0.1299 WHERE id_divida = 1"),
    ("TC-K07", "categoria duplicada", "ORA-00001", "UK_SF_CATEGORIA_NOME",
     "INSERT INTO T_SF_CATEGORIA (nome, tipo) VALUES ('Moradia', 'GASTO')"),
    ("TC-K08", "mesma conta cadastrada duas vezes", "ORA-00001", "UK_SF_CONTA_NUMERO",
     "INSERT INTO T_SF_CONTA_BANCARIA (id_usuario, nm_banco, tipo_conta, nr_conta) VALUES (1, 'Itaú', 'CORRENTE', '1234-5')"),
    ("TC-K09", "status de investimento fora do domínio", "ORA-02290", "CK_SF_INVEST_STATUS",
     "UPDATE T_SF_INVESTIMENTO SET status = 'ativo' WHERE id_investimento = 1"),
]

# Construções exclusivas do Oracle 23ai que quebrariam no 19c da FIAP (D-16)
PADROES_23AI = [
    (r"\bIF\s+(NOT\s+)?EXISTS\b", "IF [NOT] EXISTS"),
    (r"\bBOOLEAN\b", "tipo BOOLEAN em SQL"),
    (r"^\s*SELECT\b(?:(?!\bFROM\b).)*;\s*$", "SELECT sem FROM"),
    (r"\bGROUP\s+BY\s+(ALL|\d)", "GROUP BY ALL/posicional"),
    (r"\bVECTOR\b|\bJSON\s+RELATIONAL\s+DUALITY\b", "tipos 23ai"),
    (r"\bDEFAULT\s+ON\s+NULL\s+FOR\s+INSERT\b", "DEFAULT ON NULL FOR INSERT (23ai)"),
]
ARQUIVOS = ["database/ddl/00-drop-tables.sql", "database/ddl/01-create-tables.sql",
            "database/dml/02-seed.sql", "database/comandos/fintech-comandos.sql"]


def main():
    con = t.conectar()
    t.log("\n## Constraints do DDL (testes negativos)")
    for caso, desc, ora, cons, sql in CASOS:
        if ora:
            ok, msg = t.em_savepoint(con, lambda cur: t.espera_erro(cur, sql, ora, cons))
            t.registrar(caso, desc, f"{ora} {cons}", msg, ok)
        else:
            def aceita(cur):
                try:
                    cur.execute(sql)
                    return True, f"{cur.rowcount} linha(s)"
                except Exception as e:  # noqa: BLE001
                    return False, str(e).splitlines()[0]
            ok, msg = t.em_savepoint(con, aceita)
            t.registrar(caso, desc, "aceito", msg, ok)
    con.rollback()

    t.log("\n## Compatibilidade Oracle 19c (D-16) — revisão estática")
    achados = []
    for arq in ARQUIVOS:
        texto = re.sub(r"--[^\n]*", "", (t.RAIZ / arq).read_text(encoding="utf-8"))
        for stmt in texto.split(";"):
            for padrao, nome in PADROES_23AI:
                if re.search(padrao, stmt.strip() + ";", re.I | re.S | re.M):
                    achados.append(f"{arq}: {nome}")
    t.registrar("TC-V01", "nenhuma construção exclusiva do 23ai nos scripts", "0 ocorrências",
                f"{len(achados)} ocorrências {achados or ''}", not achados)

    total = len(t.RESULTADOS)
    ok = sum(r.passou for r in t.RESULTADOS)
    t.log(f"\nRESULTADO: {ok}/{total} passaram")
    return t.RESULTADOS


if __name__ == "__main__":
    res = main()
    sys.exit(0 if all(r.passou for r in res) else 1)
