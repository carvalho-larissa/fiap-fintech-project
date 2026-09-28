# Relatório de testes — comandos SQL Fintech (T13)

| Item | Valor |
|---|---|
| Data | 2026-09-27 21:04 |
| Execução | tudo |
| Resultado | **50/50 passaram** |

Gerado por `database/testes/executar_testes.py`. Cada comando testado é o comando do entregável (`database/comandos/fintech-comandos.sql`) com as máscaras substituídas por valores — sem reescrita.

| Caso | Descrição | Esperado | Obtido | Resultado |
|---|---|---|---|---|
| TC-E01 | tabelas T_SF_* | 10 | 10 | ✅ Passou |
| TC-E02 | objetos inválidos | 0 | 0 | ✅ Passou |
| TC-E03 | constraints PK/FK/UK sem nome gerado pelo sistema | 0 | 0 | ✅ Passou |
| TC-E04 | FKs no banco = FKs do dicionário (mesmos nomes) | 13 FKs | 13 FKs; divergências: nenhuma | ✅ Passou |
| TC-E05 | índices IX_SF_* | 11 | 11 | ✅ Passou |
| TC-E06 | colunas IDENTITY | 10 | 10 | ✅ Passou |
| TC-C01 | novo usuário válido | 1 linha; id 5; dt_cadastro hoje; ativo S | 1 linha; [(5, 'hoje', 'S')] | ✅ Passou |
| TC-C02 | e-mail duplicado | ORA-00001 UK_SF_USUARIO_EMAIL | ORA-00001: unique constraint (FINTECH.UK_SF_USUARIO_EMAIL) violated on table FINTECH.T_SF_USUARIO columns (EMAIL) | ✅ Passou |
| TC-C03 | conta para usuário existente | 1 linha; id 6; ativa S | 1; [(6, 'S')] | ✅ Passou |
| TC-C04 | conta para usuário inexistente | ORA-02291 FK_SF_CONTA_USUARIO | ORA-02291: integrity constraint (FINTECH.FK_SF_CONTA_USUARIO) violated - parent key not found | ✅ Passou |
| TC-C05 | receita válida | 1 linha; id 3; 750; 20/10/2025 | 1; [(3, 750, '20/10/2025')] | ✅ Passou |
| TC-C06 | gasto válido (comprovante nulo) | 1 linha; id 7; VARIAVEL; NULL | 1; [(7, 'VARIAVEL', None)] | ✅ Passou |
| TC-C07 | gasto com tipo fora do domínio ('fixo') | ORA-02290 CK_SF_GASTO_TIPO | ORA-02290: check constraint (FINTECH.CK_SF_GASTO_TIPO) violated | ✅ Passou |
| TC-C07b | gasto do usuário 1 na conta do usuário 2 (D-14) | ORA-02291 FK_SF_GASTO_CONTA | ORA-02291: integrity constraint (FINTECH.FK_SF_GASTO_CONTA) violated - parent key not found | ✅ Passou |
| TC-C08 | investimento válido sem vencimento | 1 linha; id 6; ATIVO; 0.0617; NULL | 1; [(6, 'ATIVO', Decimal('0.0617'), None)] | ✅ Passou |
| TC-A01 | alterar usuário 4 | 1 linha; só o usuário 4 muda; senha e dt_cadastro intactos | 1 linha; linhas alteradas: [4] | ✅ Passou |
| TC-A02 | alterar e-mail para um já usado | ORA-00001 UK_SF_USUARIO_EMAIL | ORA-00001: unique constraint (FINTECH.UK_SF_USUARIO_EMAIL) violated on table FINTECH.T_SF_USUARIO columns (EMAIL) | ✅ Passou |
| TC-A03 | alterar receita 2 do usuário 1 | 1 linha; 1350; 04/10/2025 | 1; [(1350, '04/10/2025')] | ✅ Passou |
| TC-A04 | alterar receita 2 informando usuário 2 | 0 linhas | 0 linhas | ✅ Passou |
| TC-A05 | alterar gasto 3 do usuário 1 | 1 linha; só o gasto 3 muda | 1 linha; alterados [3] | ✅ Passou |
| TC-A06 | alterar gasto 3 informando usuário 2 | 0 linhas | 0 linhas | ✅ Passou |
| TC-A07 | resgatar investimento 1 do usuário 1 | 1 linha; RESGATADO | 1; [('RESGATADO',)] | ✅ Passou |
| TC-S01 | usuário 1 (sem senha) | 1 linha: 1, Larissa..., larissa@exemplo.com, NULL, 01/03/2025, S; sem coluna senha | [(1, 'Larissa Gomes de Carvalho', 'larissa@exemplo.com', None, '01/03/2025', 'S')]; colunas ['id_usuario', 'nome', 'email', 'avatar', 'dt_cadastro', 'ativo'] | ✅ Passou |
| TC-S02 | gasto 4 do usuário 1 | (4, 1, 1, 4, Mercado extra, 412.30, 09/10/2025, VARIAVEL, NULL) | [(4, 1, 1, 4, 'Mercado extra', Decimal('412.3'), '09/10/2025', 'VARIAVEL', None)] | ✅ Passou |
| TC-S03 | gasto 4 informando usuário 2 | 0 linhas | 0 linhas | ✅ Passou |
| TC-S04a | investimento 2 do usuário 1 | Tesouro Selic 2029, 1500, 0.1075, 15/09/2025, 01/03/2029, ATIVO | [(2, 1, 2, 'Tesouro Selic 2029', 'TESOURO', 'Tesouro Nacional', 1500, Decimal('0.1075'), '15/09/2025', '01/03/2029', 'ATIVO')] | ✅ Passou |
| TC-S04b | investimento 999 | 0 linhas | 0 linhas | ✅ Passou |
| TC-O01a | despesas do usuário 1 | [4, 3, 1, 2] | [4, 3, 1, 2] | ✅ Passou |
| TC-O01b | despesas do usuário 2 | [6, 5] | [6, 5] | ✅ Passou |
| TC-O01c | despesas do usuário 3 | [] | [] | ✅ Passou |
| TC-O02a | investimentos do usuário 1 | [3, 2, 1] | [3, 2, 1] | ✅ Passou |
| TC-O02b | investimentos do usuário 3 | [5, 4] | [5, 4] | ✅ Passou |
| TC-O02c | investimentos do usuário 2 | [] | [] | ✅ Passou |
| TC-D01 | dashboard usuário 1 (usuário completo; empates resolvidos pelo maior ID) | 1 linha; gasto 4; investimento 3 | 1 linha(s); gasto 4; investimento 3 | ✅ Passou |
| TC-D02 | dashboard usuário 1 escolhe maior ID em empate de data | gasto 4 (não 3); investimento 3 (não 2) | gasto 4; investimento 3 | ✅ Passou |
| TC-D06b | isolamento: dados de outros usuários não vazam para o usuário 1 | gasto != 6; investimento != 5 | gasto 4; investimento 3 | ✅ Passou |
| TC-D03 | dashboard usuário 2 (sem investimentos) | 1 linha; gasto 6; investimento None | 1 linha(s); gasto 6; investimento None | ✅ Passou |
| TC-D04 | dashboard usuário 3 (sem gastos) | 1 linha; gasto None; investimento 5 | 1 linha(s); gasto None; investimento 5 | ✅ Passou |
| TC-D05 | dashboard usuário 4 (sem movimentação) | 1 linha; gasto None; investimento None | 1 linha(s); gasto None; investimento None | ✅ Passou |
| TC-D06 | dashboard usuário inexistente | 0 linhas | 0 linhas | ✅ Passou |
| TC-K01 | valor de gasto negativo | ORA-02290 CK_SF_GASTO_VALOR | ORA-02290: check constraint (FINTECH.CK_SF_GASTO_VALOR) violated | ✅ Passou |
| TC-K02 | parcela PAGA sem data de pagamento (D-15) | ORA-02290 CK_SF_PARCELA_PAGAMENTO | ORA-02290: check constraint (FINTECH.CK_SF_PARCELA_PAGAMENTO) violated | ✅ Passou |
| TC-K03 | parcela PENDENTE sem data de pagamento é aceita (D-15) | aceito | 1 linha(s) | ✅ Passou |
| TC-K04 | vencimento anterior à aplicação | ORA-02290 CK_SF_INVEST_DT_VENCIMENTO | ORA-02290: check constraint (FINTECH.CK_SF_INVEST_DT_VENCIMENTO) violated | ✅ Passou |
| TC-K05 | e-mail sem formato válido | ORA-02290 CK_SF_USUARIO_EMAIL | ORA-02290: check constraint (FINTECH.CK_SF_USUARIO_EMAIL) violated | ✅ Passou |
| TC-K06 | taxa de juros de cartão 12,99% a.m. cabe em NUMBER(5,4) como fração (D-17) | aceito | 1 linha(s) | ✅ Passou |
| TC-K07 | categoria duplicada | ORA-00001 UK_SF_CATEGORIA_NOME | ORA-00001: unique constraint (FINTECH.UK_SF_CATEGORIA_NOME) violated on table FINTECH.T_SF_CATEGORIA columns (NOME, TIPO) | ✅ Passou |
| TC-K08 | mesma conta cadastrada duas vezes | ORA-00001 UK_SF_CONTA_NUMERO | ORA-00001: unique constraint (FINTECH.UK_SF_CONTA_NUMERO) violated on table FINTECH.T_SF_CONTA_BANCARIA columns (ID_USUARIO, NM_BANCO, NR_CONTA) | ✅ Passou |
| TC-K09 | status de investimento fora do domínio | ORA-02290 CK_SF_INVEST_STATUS | ORA-02290: check constraint (FINTECH.CK_SF_INVEST_STATUS) violated | ✅ Passou |
| TC-V01 | nenhuma construção exclusiva do 23ai nos scripts | 0 ocorrências | 0 ocorrências  | ✅ Passou |
