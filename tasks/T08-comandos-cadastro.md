# T08 — Comandos de cadastro (5 INSERT)

| Campo | Valor |
|---|---|
| Status | 🟨 Escrito — verificação estática OK; aguarda execução no Oracle (T13) |
| Tamanho | M |
| Depende de | T03 |
| Bloqueia | T13 |
| Requisitos | RF-01 a RF-05, RNF-03, RNF-04, RNF-07 |

## Objetivo
Escrever os 5 comandos de cadastro exigidos, com máscaras de substituição no padrão do enunciado.

## Especificação
Arquivo: `database/comandos/fintech-comandos.sql`, seção **1. CADASTRO**.

Regras comuns:
- Lista de colunas **sempre explícita**; coluna de ID **omitida** (gerada por `IDENTITY`, D-02).
- Máscara TEXTO → `'[NOME DO CAMPO]'`; NUMÉRICO → `[NOME DO CAMPO]` (sem aspas); DATA → `TO_DATE('[DATA DO X]', 'DD/MM/YYYY')` (D-03).
- Nome da máscara em MAIÚSCULAS e em português de negócio (ex.: `[VALOR DO GASTO]`, não `[vl_gasto]`).
- Colunas com default de sistema (`dt_cadastro`, `ativo`, `ativa`, `status` de investimento) recebem valor explícito (`SYSDATE`, `'S'`, `'ATIVO'`) para deixar o comando autoexplicativo.
- Sem `COMMIT` (D-07).

| Item | Tabela | Colunas informadas pelo usuário | Valores fixos |
|---|---|---|---|
| 1.1 Novo usuário (RF-01) | `T_SF_USUARIO` | nome, email, senha, avatar | `dt_cadastro = SYSDATE`, `ativo = 'S'` |
| 1.2 Conta bancária (RF-02) | `T_SF_CONTA_BANCARIA` | id_usuario, nm_banco, tipo_conta, nr_conta | `ativa = 'S'` |
| 1.3 Nova receita (RF-03) | `T_SF_RECEITA` | id_usuario, id_conta, id_categoria, descricao, valor, dt_recebimento, origem, recorrencia, comprovante | — |
| 1.4 Nova despesa (RF-04) | `T_SF_GASTO` | id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante | — |
| 1.5 Novo investimento (RF-05) | `T_SF_INVESTIMENTO` | id_usuario, id_conta, nm_investimento, tipo, instituicao, vl_aplicado, tx_rentabilidade, dt_aplicacao, dt_vencimento | `status = 'ATIVO'` |

Exemplo de forma esperada (referência de estilo, não versão final):
```sql
INSERT INTO T_SF_GASTO (id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante)
VALUES ([CÓDIGO DO USUÁRIO], [CÓDIGO DA CONTA], [CÓDIGO DA CATEGORIA], '[DESCRIÇÃO DO GASTO]',
        [VALOR DO GASTO], TO_DATE('[DATA DO GASTO]', 'DD/MM/YYYY'), '[TIPO DO GASTO]', '[CAMINHO DO COMPROVANTE]');
```

## Critérios de aceitação
- [ ] 5 comandos, cada um precedido do título do enunciado (ex.: `-- 1.4 Cadastrar os dados de uma nova despesa (gasto) de um usuário`)
- [ ] Toda coluna NOT NULL sem default aparece no `INSERT`
- [ ] Nenhum número entre aspas; todo texto entre aspas; toda data com `TO_DATE`
- [ ] Nomes de tabela/coluna idênticos ao DDL (T06)
- [ ] Casos de teste TC-C01 a TC-C08 aprovados em T13

## Casos de teste (executados em T13)
- TC-C01 Inserir usuário válido → 1 linha, ID gerado, `dt_cadastro` = hoje
- TC-C02 Inserir usuário com e-mail repetido → `ORA-00001` (D-13)
- TC-C03 Inserir conta para usuário existente → 1 linha
- TC-C04 Inserir conta para usuário inexistente → `ORA-02291` (FK)
- TC-C05 Inserir receita válida → 1 linha
- TC-C06 Inserir gasto válido → 1 linha
- TC-C07 Inserir gasto com tipo fora do domínio (`'fixo'`) → `ORA-02290` (CHECK)
- TC-C08 Inserir investimento válido → 1 linha, `status = 'ATIVO'`

## Artefatos de saída
- `database/comandos/fintech-comandos.sql` (seção 1)
