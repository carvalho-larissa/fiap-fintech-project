-- =============================================================================
-- Sistema Fintech (SF) — Comandos SQL da atividade (Fase 4) — ENTREGÁVEL
-- -----------------------------------------------------------------------------
-- Comandos que a aplicação Java executará via JDBC. Máscaras:
--   TEXTO    -> '[NOME DO CAMPO]'
--   NUMÉRICO -> [NOME DO CAMPO]
--   DATA     -> TO_DATE('[DATA DO CAMPO]', 'DD/MM/YYYY')              (D-03)
--
-- Regras (docs/05-banco-de-dados/decisoes-tecnicas.md):
--   - IDs gerados por IDENTITY: nenhum INSERT informa a coluna de ID   (D-02)
--   - Domínios em maiúsculas, sem acento (ex.: 'VARIAVEL')             (D-04)
--   - A senha nunca é retornada nem alterada pelo UPDATE de perfil     (D-05)
--   - Sem COMMIT: a transação é controlada pela aplicação              (D-07)
--   - "Mais recente" = data DESC, id DESC                              (D-08)
--   - Taxas em fração decimal: 0.0299 = 2,99%                          (D-17)
--
-- Tabelas: database/ddl/01-create-tables.sql
-- Autora : Larissa Gomes de Carvalho — RM 571266 — 1TDSOA
-- =============================================================================


-- =============================================================================
-- 1. CADASTRO
-- =============================================================================

-- 1.1 Cadastrar os dados de um novo usuário
INSERT INTO T_SF_USUARIO (nome, email, senha, avatar, dt_cadastro, ativo)
VALUES ('[NOME DO USUÁRIO]', '[E-MAIL DO USUÁRIO]', '[HASH DA SENHA]',
        '[CAMINHO DO AVATAR]', SYSDATE, 'S');

-- 1.2 Cadastrar os dados da conta bancária de um usuário
INSERT INTO T_SF_CONTA_BANCARIA (id_usuario, nm_banco, tipo_conta, nr_conta,
                                 ativa)
VALUES ([CÓDIGO DO USUÁRIO], '[NOME DO BANCO]', '[TIPO DA CONTA]',
        '[NÚMERO DA CONTA]', 'S');

-- 1.3 Cadastrar os dados de uma nova receita (entrada de dinheiro) para um usuário
INSERT INTO T_SF_RECEITA (id_usuario, id_conta, id_categoria, descricao,
                          valor, dt_recebimento, origem, recorrencia,
                          comprovante)
VALUES ([CÓDIGO DO USUÁRIO], [CÓDIGO DA CONTA], [CÓDIGO DA CATEGORIA],
        '[DESCRIÇÃO DA RECEITA]', [VALOR DA RECEITA],
        TO_DATE('[DATA DO RECEBIMENTO]', 'DD/MM/YYYY'),
        '[ORIGEM DA RECEITA]', '[RECORRÊNCIA DA RECEITA]',
        '[CAMINHO DO COMPROVANTE]');

-- 1.4 Cadastrar os dados de uma nova despesa (gasto) de um usuário
INSERT INTO T_SF_GASTO (id_usuario, id_conta, id_categoria, descricao, valor,
                        dt_gasto, tipo, comprovante)
VALUES ([CÓDIGO DO USUÁRIO], [CÓDIGO DA CONTA], [CÓDIGO DA CATEGORIA],
        '[DESCRIÇÃO DO GASTO]', [VALOR DO GASTO],
        TO_DATE('[DATA DO GASTO]', 'DD/MM/YYYY'),
        '[TIPO DO GASTO]', '[CAMINHO DO COMPROVANTE]');

-- 1.5 Cadastrar os dados de um novo investimento feito por um usuário
INSERT INTO T_SF_INVESTIMENTO (id_usuario, id_conta, nm_investimento, tipo,
                               instituicao, vl_aplicado, tx_rentabilidade,
                               dt_aplicacao, dt_vencimento, status)
VALUES ([CÓDIGO DO USUÁRIO], [CÓDIGO DA CONTA], '[NOME DO INVESTIMENTO]',
        '[TIPO DO INVESTIMENTO]', '[INSTITUIÇÃO]', [VALOR APLICADO],
        [TAXA DE RENTABILIDADE],
        TO_DATE('[DATA DA APLICAÇÃO]', 'DD/MM/YYYY'),
        TO_DATE('[DATA DE VENCIMENTO]', 'DD/MM/YYYY'), 'ATIVO');


-- =============================================================================
-- 2. ALTERAÇÃO
-- =============================================================================

-- 2.1 Alterar os dados de um usuário (a partir do código do usuário)
UPDATE T_SF_USUARIO
   SET nome   = '[NOME DO USUÁRIO]',
       email  = '[E-MAIL DO USUÁRIO]',
       avatar = '[CAMINHO DO AVATAR]'
 WHERE id_usuario = [CÓDIGO DO USUÁRIO];

-- 2.2 Alterar os dados de uma receita (a partir do código do usuário e do código da receita)
UPDATE T_SF_RECEITA
   SET id_conta       = [CÓDIGO DA CONTA],
       id_categoria   = [CÓDIGO DA CATEGORIA],
       descricao      = '[DESCRIÇÃO DA RECEITA]',
       valor          = [VALOR DA RECEITA],
       dt_recebimento = TO_DATE('[DATA DO RECEBIMENTO]', 'DD/MM/YYYY'),
       origem         = '[ORIGEM DA RECEITA]',
       recorrencia    = '[RECORRÊNCIA DA RECEITA]',
       comprovante    = '[CAMINHO DO COMPROVANTE]'
 WHERE id_receita = [CÓDIGO DA RECEITA]
   AND id_usuario = [CÓDIGO DO USUÁRIO];

-- 2.3 Alterar os dados de uma despesa (a partir do código do usuário e do código da despesa)
UPDATE T_SF_GASTO
   SET id_conta     = [CÓDIGO DA CONTA],
       id_categoria = [CÓDIGO DA CATEGORIA],
       descricao    = '[DESCRIÇÃO DO GASTO]',
       valor        = [VALOR DO GASTO],
       dt_gasto     = TO_DATE('[DATA DO GASTO]', 'DD/MM/YYYY'),
       tipo         = '[TIPO DO GASTO]',
       comprovante  = '[CAMINHO DO COMPROVANTE]'
 WHERE id_gasto   = [CÓDIGO DO GASTO]
   AND id_usuario = [CÓDIGO DO USUÁRIO];

-- 2.4 Alterar os dados de um investimento (a partir do código do usuário e do código do investimento)
UPDATE T_SF_INVESTIMENTO
   SET id_conta         = [CÓDIGO DA CONTA],
       nm_investimento  = '[NOME DO INVESTIMENTO]',
       tipo             = '[TIPO DO INVESTIMENTO]',
       instituicao      = '[INSTITUIÇÃO]',
       vl_aplicado      = [VALOR APLICADO],
       tx_rentabilidade = [TAXA DE RENTABILIDADE],
       dt_aplicacao     = TO_DATE('[DATA DA APLICAÇÃO]', 'DD/MM/YYYY'),
       dt_vencimento    = TO_DATE('[DATA DE VENCIMENTO]', 'DD/MM/YYYY'),
       status           = '[STATUS DO INVESTIMENTO]'
 WHERE id_investimento = [CÓDIGO DO INVESTIMENTO]
   AND id_usuario      = [CÓDIGO DO USUÁRIO];


-- =============================================================================
-- 3. CONSULTAS SIMPLES
-- =============================================================================

-- 3.1 Consultar os dados de um usuário específico (usando o código dele)
SELECT id_usuario, nome, email, avatar, dt_cadastro, ativo
  FROM T_SF_USUARIO
 WHERE id_usuario = [CÓDIGO DO USUÁRIO];

-- 3.2 Consultar os dados de uma despesa específica (usando o código do usuário e o da despesa)
SELECT id_gasto, id_usuario, id_conta, id_categoria, descricao, valor,
       dt_gasto, tipo, comprovante
  FROM T_SF_GASTO
 WHERE id_gasto   = [CÓDIGO DO GASTO]
   AND id_usuario = [CÓDIGO DO USUÁRIO];

-- 3.3 Consultar os dados de um investimento específico (com código do usuário e do investimento)
SELECT id_investimento, id_usuario, id_conta, nm_investimento, tipo,
       instituicao, vl_aplicado, tx_rentabilidade, dt_aplicacao,
       dt_vencimento, status
  FROM T_SF_INVESTIMENTO
 WHERE id_investimento = [CÓDIGO DO INVESTIMENTO]
   AND id_usuario      = [CÓDIGO DO USUÁRIO];


-- =============================================================================
-- 4. CONSULTAS ORDENADAS
-- =============================================================================

-- 4.1 Consultar todas as despesas de um usuário, ordenadas da mais recente à mais antiga
SELECT id_gasto, id_usuario, id_conta, id_categoria, descricao, valor,
       dt_gasto, tipo, comprovante
  FROM T_SF_GASTO
 WHERE id_usuario = [CÓDIGO DO USUÁRIO]
 ORDER BY dt_gasto DESC, id_gasto DESC;

-- 4.2 Consultar todos os investimentos de um usuário, do mais recente ao mais antigo
SELECT id_investimento, id_usuario, id_conta, nm_investimento, tipo,
       instituicao, vl_aplicado, tx_rentabilidade, dt_aplicacao,
       dt_vencimento, status
  FROM T_SF_INVESTIMENTO
 WHERE id_usuario = [CÓDIGO DO USUÁRIO]
 ORDER BY dt_aplicacao DESC, id_investimento DESC;


-- =============================================================================
-- 5. CONSULTA PARA O DASHBOARD
-- =============================================================================

-- 5.1 Consultar as informações principais de um usuário, junto com a última despesa e o último investimento deste usuário (retorna apenas uma linha)
--     Lógica: ROW_NUMBER() numera despesas e investimentos do usuário do
--     mais recente ao mais antigo (data DESC, id DESC) e fica só com o nº 1
--     de cada. LEFT JOIN mantém a linha do usuário mesmo sem despesa ou
--     investimento (colunas nulas). Um único registro de cada lado garante
--     uma linha só, sem produto cartesiano.
SELECT u.id_usuario,
       u.nome,
       u.email,
       u.dt_cadastro,
       g.id_gasto        AS id_ultimo_gasto,
       g.descricao       AS descricao_ultimo_gasto,
       g.valor           AS valor_ultimo_gasto,
       g.dt_gasto        AS dt_ultimo_gasto,
       g.tipo            AS tipo_ultimo_gasto,
       i.id_investimento AS id_ultimo_investimento,
       i.nm_investimento AS nm_ultimo_investimento,
       i.tipo            AS tipo_ultimo_investimento,
       i.vl_aplicado     AS vl_ultimo_investimento,
       i.dt_aplicacao    AS dt_ultimo_investimento
  FROM T_SF_USUARIO u
  LEFT JOIN (SELECT id_usuario, id_gasto, descricao, valor, dt_gasto, tipo,
                    ROW_NUMBER() OVER (ORDER BY dt_gasto DESC,
                                                id_gasto DESC) AS rn
               FROM T_SF_GASTO
              WHERE id_usuario = [CÓDIGO DO USUÁRIO]) g
         ON g.id_usuario = u.id_usuario
        AND g.rn = 1
  LEFT JOIN (SELECT id_usuario, id_investimento, nm_investimento, tipo,
                    vl_aplicado, dt_aplicacao,
                    ROW_NUMBER() OVER (ORDER BY dt_aplicacao DESC,
                                                id_investimento DESC) AS rn
               FROM T_SF_INVESTIMENTO
              WHERE id_usuario = [CÓDIGO DO USUÁRIO]) i
         ON i.id_usuario = u.id_usuario
        AND i.rn = 1
 WHERE u.id_usuario = [CÓDIGO DO USUÁRIO];
