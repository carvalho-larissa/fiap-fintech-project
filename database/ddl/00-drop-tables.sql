-- =============================================================================
-- Sistema Fintech (SF) — 00-drop-tables.sql
-- -----------------------------------------------------------------------------
-- Remove todas as tabelas do modelo (ordem reversa de dependência).
-- Idempotente: ignora ORA-00942 (tabela inexistente). Compatível com Oracle 19c
-- (não usa DROP TABLE IF EXISTS, exclusivo do 23ai — decisão D-16).
-- As sequences internas das colunas IDENTITY são removidas junto com a tabela.
--
-- Autora : Larissa Gomes de Carvalho — RM 571266 — 1TDSOA
-- Versão : 2.0 (Fase 4)
-- Ordem  : 00-drop-tables.sql -> 01-create-tables.sql -> 02-seed.sql
-- =============================================================================
SET DEFINE OFF
SET SERVEROUTPUT ON

DECLARE
    TYPE t_lista IS TABLE OF VARCHAR2(30);
    v_tabelas t_lista := t_lista(
        'T_SF_APORTE_META',
        'T_SF_PARCELA',
        'T_SF_INVESTIMENTO',
        'T_SF_GASTO',
        'T_SF_RECEITA',
        'T_SF_META',
        'T_SF_DIVIDA',
        'T_SF_CONTA_BANCARIA',
        'T_SF_CATEGORIA',
        'T_SF_USUARIO'
    );
BEGIN
    FOR i IN 1 .. v_tabelas.COUNT LOOP
        BEGIN
            EXECUTE IMMEDIATE 'DROP TABLE ' || v_tabelas(i) || ' CASCADE CONSTRAINTS PURGE';
            DBMS_OUTPUT.PUT_LINE('Removida: ' || v_tabelas(i));
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE = -942 THEN
                    DBMS_OUTPUT.PUT_LINE('Inexistente (ignorada): ' || v_tabelas(i));
                ELSE
                    RAISE;
                END IF;
        END;
    END LOOP;
END;
/
