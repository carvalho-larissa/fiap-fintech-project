# AGENTS.md — Projeto Fintech (FIAP)

Guia rápido para pessoas e agentes de IA que trabalham neste repositório.

## Sobre o projeto

Aplicação de **gestão financeira pessoal** ("Sistema Fintech", prefixo `SF`),
desenvolvida como projeto acadêmico da FIAP (Turma 1TDSOA — Larissa Gomes de Carvalho, RM 571266).

Épico: *Gerenciamento do fluxo de caixa e patrimônio.* O usuário cadastra perfil e
contas bancárias, registra receitas e gastos (fixos/variáveis), controla dívidas
(parcelas, juros, atrasos) e acompanha metas financeiras (aportes e progresso).

Prioridade do MVP (definida na especificação de requisitos):
1. Cadastro de perfil → 2. Receitas → 3. Gastos → 4. Metas → 5. Dívidas

Estado atual: documentação de análise concluída, protótipo front-end estático
(HTML + Tailwind) e modelo de domínio em Java (métodos de negócio ainda são stubs
que apenas imprimem mensagens). Ainda **não há** persistência, API nem integração
front ↔ back.

## Estrutura

```
projeto-fintech/
├── AGENTS.md                  # este arquivo
├── .gitignore
├── docs/                      # artefatos de análise e design (fonte da verdade dos requisitos)
│   ├── 01-requisitos/
│   │   └── especificacao-de-requisitos-com-user-stories.docx   # épico, 5 user stories, critérios de aceitação, INVEST, priorização
│   ├── 02-casos-de-uso/
│   │   └── modelagem-casos-de-uso.pdf      # diagrama de contexto, casos de uso UC01–UC06, detalhamento do UC03
│   ├── 03-modelagem-de-dados/
│   │   └── modelagem-de-dados.pdf          # modelo lógico e físico (Oracle) — tabelas T_SF_*
│   └── 04-prototipos-interface/
│       └── interfaces.pdf                  # 5 telas do protótipo (dashboard, receitas, gastos, dívidas, metas)
├── frontend/                  # protótipo estático, sem build
│   ├── index.html             # Dashboard (saldo, fluxo de caixa, categorias, últimas transações)
│   ├── receitas.html          # Cadastro de receita
│   ├── gastos.html            # Cadastro de gasto
│   ├── dividas.html           # Gestão de dívidas
│   ├── metas.html             # Metas financeiras
│   └── css/styles.css         # CSS customizado (fonte Inter, scrollbar, foco, reduced-motion)
└── backend/                   # modelo de domínio em Java (projeto IntelliJ "metodos-em-java")
    ├── metodos-em-java.iml
    ├── .idea/                 # config do IntelliJ (workspace.xml é local e ignorado pelo git)
    └── src/                   # pacote default
        ├── Main.java          # demonstração: instancia cada entidade e chama seus métodos
        ├── Usuario.java       # cadastrarUsuario, validarEmail, atualizarPerfil
        ├── ContaBancaria.java # vincularConta, consultarSaldo, desativarConta
        ├── Receita.java       # registrarReceita, editarReceita, calcularTotalReceitas
        ├── Gasto.java         # registrarGasto, categorizarGasto, calcularImpactoNoSaldo
        ├── Divida.java        # registrarParcelaAtraso, calcularJuros, exibirAlertaVencimento
        └── Meta.java          # criarMeta, registrarAporte, calcularProgresso, validarOrcamentoDisponivel
```

## Rastreabilidade (requisito → dados → código → tela)

| User Story            | Tabela(s)                          | Classe Java     | Tela             |
|-----------------------|------------------------------------|-----------------|------------------|
| 1. Cadastro de perfil | T_SF_USUARIO, T_SF_CONTA_BANCARIA  | Usuario, ContaBancaria | —         |
| 2. Receitas           | T_SF_RECEITA, T_SF_CATEGORIA       | Receita         | receitas.html    |
| 3. Gastos             | T_SF_GASTO, T_SF_CATEGORIA         | Gasto           | gastos.html      |
| 4. Dívidas            | T_SF_DIVIDA, T_SF_PARCELA          | Divida          | dividas.html     |
| 5. Metas              | T_SF_META, T_SF_APORTE_META        | Meta            | metas.html       |
| (visão consolidada)   | todas                              | —               | index.html       |

Lacunas conhecidas: `T_SF_CATEGORIA`, `T_SF_PARCELA` e `T_SF_APORTE_META` ainda não
têm classe Java; não existe tela de cadastro de perfil.

## Como executar

Front-end: abrir `frontend/index.html` no navegador (Tailwind via CDN — requer internet).

Back-end (JDK 25+; o projeto IntelliJ usa language level 25):
```bash
cd backend
javac -encoding UTF-8 -d out src/*.java
java -cp out Main
```
Ou abrir a pasta `backend/` no IntelliJ e executar `Main`.

## Convenções

- Idioma do domínio, código e documentação: **português (pt-BR)**.
- Java: classes em PascalCase, atributos/métodos em camelCase; nomes de atributos
  espelham as colunas do modelo de dados (`id_usuario` → `idUsuario`).
- Banco: tabelas `T_SF_<ENTIDADE>`, PK `id_<entidade>`, prefixos `vl_` (valor),
  `dt_` (data), `nr_` (número), `tx_` (taxa); booleanos como `CHAR(1)`.
- Front-end: layout via classes Tailwind no HTML; `css/styles.css` só para
  melhorias globais. Cores da marca: `brand #15454e`, `emerald2 #10b981`.
- Artefatos gerados (`backend/out/`, `*.class`) não são versionados.
- Novos documentos de análise vão em `docs/NN-<tema>/`, mantendo a numeração por fase.
