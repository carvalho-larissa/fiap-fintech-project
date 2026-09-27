-- =============================================================================
-- Sistema Fintech (SF) — 02-seed.sql
-- -----------------------------------------------------------------------------
-- Massa de dados DETERMINÍSTICA para validar os comandos da atividade (T13).
-- IDs explícitos (permitido por IDENTITY BY DEFAULT — D-02); ao final, as
-- identities são reposicionadas para continuar após o maior ID carregado.
-- Resultados esperados: database/testes/resultados-esperados.md
--
-- Cenários:
--   U1 Larissa  — gastos e investimentos, com EMPATE de data (desempate D-08)
--   U2 Bruno    — só gastos (dashboard com investimento nulo); tem o gasto mais
--                 recente de todo o banco (prova de isolamento por usuário)
--   U3 Carla    — só investimentos (dashboard com gasto nulo)
--   U4 Diego    — sem movimentação (dashboard só com dados do usuário)
--   999         — inexistente (consultas devem retornar 0 linhas)
--
-- Autora : Larissa Gomes de Carvalho — RM 571266 — 1TDSOA
-- Ordem  : 00-drop-tables.sql -> 01-create-tables.sql -> 02-seed.sql
-- =============================================================================
SET DEFINE OFF
ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';

-- -----------------------------------------------------------------------------
-- Usuários (senha = hash BCrypt fictício; nunca senha em texto puro — D-05)
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_USUARIO (id_usuario, nome, email, senha, avatar, dt_cadastro, ativo)
VALUES (1, 'Larissa Gomes de Carvalho', 'larissa@exemplo.com',
        '$2a$10$hashficticio.larissa.000000000000000000000000000000', NULL,
        TO_DATE('01/03/2025', 'DD/MM/YYYY'), 'S');
INSERT INTO T_SF_USUARIO (id_usuario, nome, email, senha, avatar, dt_cadastro, ativo)
VALUES (2, 'Bruno Almeida', 'bruno@exemplo.com',
        '$2a$10$hashficticio.bruno.00000000000000000000000000000000', NULL,
        TO_DATE('15/04/2025', 'DD/MM/YYYY'), 'S');
INSERT INTO T_SF_USUARIO (id_usuario, nome, email, senha, avatar, dt_cadastro, ativo)
VALUES (3, 'Carla Souza', 'carla@exemplo.com',
        '$2a$10$hashficticio.carla.00000000000000000000000000000000', NULL,
        TO_DATE('20/05/2025', 'DD/MM/YYYY'), 'S');
INSERT INTO T_SF_USUARIO (id_usuario, nome, email, senha, avatar, dt_cadastro, ativo)
VALUES (4, 'Diego Ramos', 'diego@exemplo.com',
        '$2a$10$hashficticio.diego.00000000000000000000000000000000', NULL,
        TO_DATE('01/10/2025', 'DD/MM/YYYY'), 'S');

-- -----------------------------------------------------------------------------
-- Categorias (alinhadas ao protótipo frontend/index.html)
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_CATEGORIA (id_categoria, nome, tipo) VALUES (1, 'Salário',     'RECEITA');
INSERT INTO T_SF_CATEGORIA (id_categoria, nome, tipo) VALUES (2, 'Freelance',   'RECEITA');
INSERT INTO T_SF_CATEGORIA (id_categoria, nome, tipo) VALUES (3, 'Moradia',     'GASTO');
INSERT INTO T_SF_CATEGORIA (id_categoria, nome, tipo) VALUES (4, 'Alimentação', 'GASTO');
INSERT INTO T_SF_CATEGORIA (id_categoria, nome, tipo) VALUES (5, 'Transporte',  'GASTO');
INSERT INTO T_SF_CATEGORIA (id_categoria, nome, tipo) VALUES (6, 'Lazer',       'GASTO');

-- -----------------------------------------------------------------------------
-- Contas bancárias
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_CONTA_BANCARIA (id_conta, id_usuario, nm_banco, tipo_conta, nr_conta, ativa)
VALUES (1, 1, 'Itaú',   'CORRENTE',     '1234-5', 'S');
INSERT INTO T_SF_CONTA_BANCARIA (id_conta, id_usuario, nm_banco, tipo_conta, nr_conta, ativa)
VALUES (2, 1, 'Nubank', 'INVESTIMENTO', '9876-0', 'S');
INSERT INTO T_SF_CONTA_BANCARIA (id_conta, id_usuario, nm_banco, tipo_conta, nr_conta, ativa)
VALUES (3, 2, 'Bradesco', 'CORRENTE',   '5555-1', 'S');
INSERT INTO T_SF_CONTA_BANCARIA (id_conta, id_usuario, nm_banco, tipo_conta, nr_conta, ativa)
VALUES (4, 3, 'Inter',  'INVESTIMENTO', '7777-2', 'S');
INSERT INTO T_SF_CONTA_BANCARIA (id_conta, id_usuario, nm_banco, tipo_conta, nr_conta, ativa)
VALUES (5, 4, 'Caixa',  'POUPANCA',     '3333-9', 'S');

-- -----------------------------------------------------------------------------
-- Receitas (U1)
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_RECEITA (id_receita, id_usuario, id_conta, id_categoria, descricao, valor,
                          dt_recebimento, origem, recorrencia, comprovante)
VALUES (1, 1, 1, 1, 'Salário Empresa XPTO', 5800.00, TO_DATE('10/10/2025', 'DD/MM/YYYY'),
        'SALARIO', 'MENSAL', NULL);
INSERT INTO T_SF_RECEITA (id_receita, id_usuario, id_conta, id_categoria, descricao, valor,
                          dt_recebimento, origem, recorrencia, comprovante)
VALUES (2, 1, 1, 2, 'Freelance design', 1200.00, TO_DATE('03/10/2025', 'DD/MM/YYYY'),
        'FREELANCE', 'UNICA', NULL);

-- -----------------------------------------------------------------------------
-- Gastos
--   U1: ids 1..4 — ids 3 e 4 no MESMO dia (09/10); o mais recente é o id 4 (D-08)
--   U2: ids 5..6 — id 6 em 20/10, mais recente que qualquer gasto de U1 (isolamento)
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_GASTO (id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES (1, 1, 1, 3, 'Aluguel apartamento', 1850.00, TO_DATE('05/10/2025', 'DD/MM/YYYY'), 'FIXO', NULL);
INSERT INTO T_SF_GASTO (id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES (2, 1, 1, 5, 'Combustível', 250.00, TO_DATE('01/10/2025', 'DD/MM/YYYY'), 'VARIAVEL', NULL);
INSERT INTO T_SF_GASTO (id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES (3, 1, 1, 4, 'Padaria', 38.50, TO_DATE('09/10/2025', 'DD/MM/YYYY'), 'VARIAVEL', NULL);
INSERT INTO T_SF_GASTO (id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES (4, 1, 1, 4, 'Mercado extra', 412.30, TO_DATE('09/10/2025', 'DD/MM/YYYY'), 'VARIAVEL', NULL);
INSERT INTO T_SF_GASTO (id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES (5, 2, 3, 3, 'Condomínio', 620.00, TO_DATE('10/10/2025', 'DD/MM/YYYY'), 'FIXO', NULL);
INSERT INTO T_SF_GASTO (id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES (6, 2, 3, 6, 'Cinema', 60.00, TO_DATE('20/10/2025', 'DD/MM/YYYY'), 'VARIAVEL', NULL);

-- -----------------------------------------------------------------------------
-- Investimentos
--   U1: ids 1..3 — ids 2 e 3 no MESMO dia (15/09); o mais recente é o id 3 (D-08)
--   U3: ids 4..5 — id 5 em 25/10, mais recente que qualquer investimento de U1
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_INVESTIMENTO (id_investimento, id_usuario, id_conta, nm_investimento, tipo, instituicao,
                               vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento, status)
VALUES (1, 1, 2, 'CDB Nubank 100% CDI', 'CDB', 'Nubank', 2000.00, 0.1050,
        TO_DATE('01/08/2025', 'DD/MM/YYYY'), TO_DATE('01/08/2027', 'DD/MM/YYYY'), 'ATIVO');
INSERT INTO T_SF_INVESTIMENTO (id_investimento, id_usuario, id_conta, nm_investimento, tipo, instituicao,
                               vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento, status)
VALUES (2, 1, 2, 'Tesouro Selic 2029', 'TESOURO', 'Tesouro Nacional', 1500.00, 0.1075,
        TO_DATE('15/09/2025', 'DD/MM/YYYY'), TO_DATE('01/03/2029', 'DD/MM/YYYY'), 'ATIVO');
INSERT INTO T_SF_INVESTIMENTO (id_investimento, id_usuario, id_conta, nm_investimento, tipo, instituicao,
                               vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento, status)
VALUES (3, 1, 2, 'FII HGLG11', 'FII', 'Nubank', 800.00, NULL,
        TO_DATE('15/09/2025', 'DD/MM/YYYY'), NULL, 'ATIVO');
INSERT INTO T_SF_INVESTIMENTO (id_investimento, id_usuario, id_conta, nm_investimento, tipo, instituicao,
                               vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento, status)
VALUES (4, 3, 4, 'LCI Inter 95% CDI', 'LCI', 'Inter', 5000.00, 0.0980,
        TO_DATE('10/10/2025', 'DD/MM/YYYY'), TO_DATE('10/10/2026', 'DD/MM/YYYY'), 'ATIVO');
INSERT INTO T_SF_INVESTIMENTO (id_investimento, id_usuario, id_conta, nm_investimento, tipo, instituicao,
                               vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento, status)
VALUES (5, 3, 4, 'Ações ITUB4', 'ACOES', 'Inter', 1000.00, NULL,
        TO_DATE('25/10/2025', 'DD/MM/YYYY'), NULL, 'ATIVO');

-- -----------------------------------------------------------------------------
-- Dívida, parcelas, meta e aporte (realismo do modelo; fora do escopo dos comandos)
-- -----------------------------------------------------------------------------
INSERT INTO T_SF_DIVIDA (id_divida, id_usuario, descricao, tipo, vl_total, saldo_devedor,
                         total_parcelas, tx_juros_mensal, status, dt_inicio)
VALUES (1, 1, 'Cartão de crédito Itaú', 'CARTAO', 1480.00, 1233.34, 6, 0.1299, 'ATRASADA',
        TO_DATE('01/07/2025', 'DD/MM/YYYY'));
INSERT INTO T_SF_PARCELA (id_parcela, id_divida, nr_parcela, vl_parcela, dt_vencimento, dt_pagamento, status)
VALUES (1, 1, 1, 246.66, TO_DATE('01/08/2025', 'DD/MM/YYYY'), TO_DATE('01/08/2025', 'DD/MM/YYYY'), 'PAGA');
INSERT INTO T_SF_PARCELA (id_parcela, id_divida, nr_parcela, vl_parcela, dt_vencimento, dt_pagamento, status)
VALUES (2, 1, 2, 246.66, TO_DATE('01/09/2025', 'DD/MM/YYYY'), NULL, 'ATRASADA');

INSERT INTO T_SF_META (id_meta, id_usuario, nome, vl_alvo, vl_acumulado, prazo, status, dt_criacao)
VALUES (1, 1, 'Viagem Europa', 12000.00, 1500.00, TO_DATE('31/12/2026', 'DD/MM/YYYY'), 'ATIVA',
        TO_DATE('01/06/2025', 'DD/MM/YYYY'));
INSERT INTO T_SF_APORTE_META (id_aporte, id_meta, valor, dt_aporte, observacao)
VALUES (1, 1, 1500.00, TO_DATE('10/06/2025', 'DD/MM/YYYY'), 'Primeiro aporte');

COMMIT;

-- -----------------------------------------------------------------------------
-- Reposiciona as identities após o maior ID carregado
-- -----------------------------------------------------------------------------
ALTER TABLE T_SF_USUARIO        MODIFY id_usuario      GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_CATEGORIA      MODIFY id_categoria    GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_CONTA_BANCARIA MODIFY id_conta        GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_RECEITA        MODIFY id_receita      GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_GASTO          MODIFY id_gasto        GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_INVESTIMENTO   MODIFY id_investimento GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_DIVIDA         MODIFY id_divida       GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_PARCELA        MODIFY id_parcela      GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_META           MODIFY id_meta         GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
ALTER TABLE T_SF_APORTE_META    MODIFY id_aporte       GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH LIMIT VALUE);
