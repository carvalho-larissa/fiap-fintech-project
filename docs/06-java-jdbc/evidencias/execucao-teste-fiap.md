# Execução do Teste na instância Oracle da FIAP — 2026-10-07

Oracle Database 19c Enterprise Edition (ORACLE.FIAP.COM.BR:1521/ORCL), JDK 21.0.12, ojdbc11 23.9.0.25.07.

```
##### TESTE DOS DAOs - SISTEMA FINTECH #####

===== USUARIO - insert() x5 e getAll() =====
  inserido: id=1 Ana Beatriz Lima
  inserido: id=2 Bruno Henrique Costa
  inserido: id=3 Carla Mendes Souza
  inserido: id=4 Diego Ramos Pereira
  inserido: id=5 Elisa Ferreira Alves

  getAll() retornou 5 usuário(s):
  ID   NOME                       E-MAIL                                       CADASTRO     ATIVO
  1    Ana Beatriz Lima           teste1.1791402160623@fintech.com             2026-10-07   S      <- novo
  2    Bruno Henrique Costa       teste2.1791402160623@fintech.com             2026-10-07   S      <- novo
  3    Carla Mendes Souza         teste3.1791402160623@fintech.com             2026-10-07   S      <- novo
  4    Diego Ramos Pereira        teste4.1791402160623@fintech.com             2026-10-07   S      <- novo
  5    Elisa Ferreira Alves       teste5.1791402160623@fintech.com             2026-10-07   S      <- novo
  [OK] getAll() contém os 5 usuários inseridos
  [OK] senha não é retornada pelo getAll()

===== CONTA BANCARIA (apoio às FKs) - insert() x2 e getAll() =====
  inseridas: id=1 (Itaú), id=2 (Nubank)

  getAll() retornou 2 conta(s):
  ID   USUARIO  BANCO        TIPO           NUMERO           ATIVA
  1    1        Itaú         CORRENTE       T02160623-1      S    
  2    1        Nubank       POUPANCA       T02160623-2      S    
  [OK] getAll() contém as 2 contas inseridas

===== CATEGORIA (apoio às FKs) - garante as categorias de gasto =====
  criada: Moradia
  criada: Alimentação
  criada: Transporte
  criada: Lazer
  criada: Saúde
  categorias de gasto disponíveis: {Transporte=3, Alimentação=2, Moradia=1, Saúde=5, Lazer=4}

===== GASTO - insert() x5 e getAll() =====
  inserido: id=1 Aluguel apartamento
  inserido: id=2 Supermercado do mês
  inserido: id=3 Internet 500MB
  inserido: id=4 Uber trabalho
  inserido: id=5 Cinema e jantar

  getAll() retornou 5 gasto(s), do mais recente ao mais antigo:
  ID   USUARIO  CONTA  CATEG  DESCRICAO                       VALOR DATA         TIPO     
  5    1        1      4      Cinema e jantar                218.00 2026-10-06   VARIAVEL   <- novo
  4    1        1      3      Uber trabalho                   87.40 2026-10-05   VARIAVEL   <- novo
  3    1        1      1      Internet 500MB                 119.90 2026-10-04   FIXO       <- novo
  2    1        1      2      Supermercado do mês            412.30 2026-10-03   VARIAVEL   <- novo
  1    1        1      1      Aluguel apartamento           1850.00 2026-10-01   FIXO       <- novo
  [OK] getAll() contém os 5 gastos inseridos
  [OK] tipo normalizado para FIXO/VARIAVEL
  [OK] getAll() ordenado do mais recente ao mais antigo

===== INVESTIMENTO - insert() x5 e getAll() =====
  inserido: id=1 CDB Banco X 110% CDI
  inserido: id=2 Tesouro Selic 2029
  inserido: id=3 PETR4 - 100 ações
  inserido: id=4 HGLG11 - 20 cotas
  inserido: id=5 Fundo DI Conservador

  getAll() retornou 5 investimento(s), do mais recente ao mais antigo:
  ID   CONTA  NOME                     TIPO             VALOR     TAXA APLICACAO    VENCIMENTO   STATUS  
  5    1      Fundo DI Conservador     FUNDO          1500.00     0.11 2026-10-06   -            ATIVO     <- novo
  4    1      HGLG11 - 20 cotas        FII            3200.00        - 2026-10-02   -            ATIVO     <- novo
  3    1      PETR4 - 100 ações        ACOES          3650.00        - 2026-09-27   -            ATIVO     <- novo
  2    1      Tesouro Selic 2029       TESOURO        3000.00   0.1075 2026-09-22   2029-10-07   ATIVO     <- novo
  1    1      CDB Banco X 110% CDI     CDB            5000.00    0.125 2026-09-17   2028-10-07   ATIVO     <- novo
  [OK] getAll() contém os 5 investimentos inseridos
  [OK] colunas opcionais nulas (taxa/vencimento) recuperadas como null

===== TRATAMENTO DE EXCEÇÕES - falhas provocadas de propósito =====
  [tratado] e-mail duplicado -> Falha ao inserir usuário: registro duplicado (ORA-00001): já existe um valor igual em uma coluna única (ex.: e-mail).
  [OK] e-mail duplicado: falha tratada (ORA-00001)
  [tratado] gasto com valor negativo (CHECK) -> Falha ao inserir gasto: valor fora do permitido por uma regra da tabela (ORA-02290, CHECK).
  [OK] gasto com valor negativo (CHECK): falha tratada (ORA-02290)
  [tratado] gasto de usuário inexistente (FK) -> Falha ao inserir gasto: referência inválida (ORA-02291): o usuário, a conta ou a categoria informada não existe.
  [OK] gasto de usuário inexistente (FK): falha tratada (ORA-02291)
  [tratado] tabela inexistente -> Falha ao consultar a tabela T_SF_TABELA_INEXISTENTE: a tabela ou view não existe (ORA-00942). Verifique se o schema foi criado.
  [OK] tabela inexistente: falha tratada (ORA-00942)
  [tratado] banco fora do ar (porta sem Oracle) -> Falha ao conectar ao banco de dados: banco de dados fora do ar ou inacessível (host, porta ou rede/VPN). ORA-12541: Não é possível estabelecer conexão. Não há listener em host 127.0.0.1 port 1. (CONNECTION_ID=ZCtZANECRUC2eSQxXkYlWg==)
https://docs.oracle.com/error-help/db/ora-12541/
  [OK] banco fora do ar (porta sem Oracle): falha tratada (ORA-12541)

===== RESUMO =====
13 verificações, 0 falha(s).
```
