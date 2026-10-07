import java.math.BigDecimal;
import java.math.RoundingMode;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Teste dos DAOs: insere 5 registros de Usuario, Gasto e Investimento (mais contas e categorias de apoio
 * às chaves estrangeiras), consulta tudo com getAll() e exercita o tratamento de exceções.
 * Execução: java -cp "out;lib/*" Teste  (configure a conexão em db.properties ou DB_URL/DB_USER/DB_PASSWORD).
 */
public class Teste {

    private static final UsuarioDAO usuarioDAO = new UsuarioDAO();
    private static final ContaBancariaDAO contaDAO = new ContaBancariaDAO();
    private static final CategoriaDAO categoriaDAO = new CategoriaDAO();
    private static final GastoDAO gastoDAO = new GastoDAO();
    private static final InvestimentoDAO investimentoDAO = new InvestimentoDAO();

    private static int verificacoes = 0;
    private static int falhas = 0;

    // Chaves criadas no teste, reaproveitadas pelas etapas seguintes e pelos cenários de erro
    private static int idUsuario1;
    private static int idConta1;
    private static int idCategoria1;
    private static String emailUsuario1;

    public static void main(String[] args) {
        System.out.println("##### TESTE DOS DAOs - SISTEMA FINTECH #####");
        String sufixo = String.valueOf(System.currentTimeMillis());

        try {
            testarUsuarios(sufixo);
            testarContas(sufixo);
            Map<String, Integer> categorias = garantirCategorias();
            testarGastos(categorias);
            testarInvestimentos();
        } catch (DaoException e) {
            falhas++;
            System.err.println("\n[ERRO] O teste foi interrompido: " + e.getMessage());
        }

        testarExcecoes();

        System.out.println("\n===== RESUMO =====");
        System.out.println(verificacoes + " verificações, " + falhas + " falha(s).");
        System.exit(falhas == 0 ? 0 : 1);
    }

    // ------------------------------------------------------------------ Usuario
    private static void testarUsuarios(String sufixo) throws DaoException {
        titulo("USUARIO - insert() x5 e getAll()");
        String[] nomes = {"Ana Beatriz Lima", "Bruno Henrique Costa", "Carla Mendes Souza", "Diego Ramos Pereira",
                "Elisa Ferreira Alves"};
        List<Integer> novos = new ArrayList<>();
        for (int i = 0; i < nomes.length; i++) {
            String email = "teste" + (i + 1) + "." + sufixo + "@fintech.com";
            Usuario u = new Usuario(0, nomes[i], email, "$2a$10$hashficticio.teste." + (i + 1));
            int id = usuarioDAO.insert(u);
            novos.add(id);
            System.out.println("  inserido: id=" + id + " " + u.getNome());
            if (i == 0) {
                idUsuario1 = id;
                emailUsuario1 = email;
            }
        }

        List<Usuario> todos = usuarioDAO.getAll();
        System.out.println("\n  getAll() retornou " + todos.size() + " usuário(s):");
        System.out.printf("  %-4s %-26s %-44s %-12s %-5s%n", "ID", "NOME", "E-MAIL", "CADASTRO", "ATIVO");
        Set<Integer> idsRecuperados = new HashSet<>();
        for (Usuario u : todos) {
            idsRecuperados.add(u.getIdUsuario());
            System.out.printf("  %-4d %-26s %-44s %-12s %-5s%s%n", u.getIdUsuario(), u.getNome(), u.getEmail(),
                    u.getDtCadastro(), u.isAtivo() ? "S" : "N", novos.contains(u.getIdUsuario()) ? "  <- novo" : "");
        }
        conferir("getAll() contém os 5 usuários inseridos", idsRecuperados.containsAll(novos));
        conferir("senha não é retornada pelo getAll()", todos.stream().allMatch(u -> u.getSenha() == null));
    }

    // ------------------------------------------------------------ ContaBancaria
    private static void testarContas(String sufixo) throws DaoException {
        titulo("CONTA BANCARIA (apoio às FKs) - insert() x2 e getAll()");
        String cauda = sufixo.substring(Math.max(0, sufixo.length() - 8));
        ContaBancaria corrente = new ContaBancaria(0, idUsuario1, "Itaú", "Corrente", "T" + cauda + "-1");
        ContaBancaria poupanca = new ContaBancaria(0, idUsuario1, "Nubank", "Poupança", "T" + cauda + "-2");
        idConta1 = contaDAO.insert(corrente);
        int idConta2 = contaDAO.insert(poupanca);
        System.out.println("  inseridas: id=" + idConta1 + " (" + corrente.getNomeBanco() + "), id=" + idConta2
                + " (" + poupanca.getNomeBanco() + ")");

        List<ContaBancaria> contas = contaDAO.getAll();
        System.out.println("\n  getAll() retornou " + contas.size() + " conta(s):");
        System.out.printf("  %-4s %-8s %-12s %-14s %-16s %-5s%n", "ID", "USUARIO", "BANCO", "TIPO", "NUMERO", "ATIVA");
        for (ContaBancaria c : contas) {
            System.out.printf("  %-4d %-8d %-12s %-14s %-16s %-5s%n", c.getIdConta(), c.getIdUsuario(), c.getNomeBanco(),
                    c.getTipoConta(), c.getNumeroConta(), c.isAtiva() ? "S" : "N");
        }
        conferir("getAll() contém as 2 contas inseridas", contas.stream()
                .map(ContaBancaria::getIdConta).toList().containsAll(List.of(idConta1, idConta2)));
    }

    // ---------------------------------------------------------------- Categoria
    private static Map<String, Integer> garantirCategorias() throws DaoException {
        titulo("CATEGORIA (apoio às FKs) - garante as categorias de gasto");
        String[] nomes = {"Moradia", "Alimentação", "Transporte", "Lazer", "Saúde"};
        Map<String, Integer> ids = new HashMap<>();
        for (Categoria c : categoriaDAO.getAll()) {
            if ("GASTO".equals(c.getTipo())) {
                ids.put(c.getNome(), c.getIdCategoria());
            }
        }
        for (String nome : nomes) {
            if (!ids.containsKey(nome)) {
                ids.put(nome, categoriaDAO.insert(new Categoria(nome, "GASTO")));
                System.out.println("  criada: " + nome);
            }
        }
        idCategoria1 = ids.get("Moradia");
        System.out.println("  categorias de gasto disponíveis: " + ids);
        return ids;
    }

    // -------------------------------------------------------------------- Gasto
    private static void testarGastos(Map<String, Integer> cat) throws DaoException {
        titulo("GASTO - insert() x5 e getAll()");
        LocalDate hoje = LocalDate.now();
        Gasto[] gastos = {
                new Gasto(idUsuario1, idConta1, cat.get("Moradia"), "Aluguel apartamento", new BigDecimal("1850.00"), hoje.minusDays(6), "Fixo"),
                new Gasto(idUsuario1, idConta1, cat.get("Alimentação"), "Supermercado do mês", new BigDecimal("412.30"), hoje.minusDays(4), "Variável"),
                new Gasto(idUsuario1, idConta1, cat.get("Moradia"), "Internet 500MB", new BigDecimal("119.90"), hoje.minusDays(3), "Fixo"),
                new Gasto(idUsuario1, idConta1, cat.get("Transporte"), "Uber trabalho", new BigDecimal("87.40"), hoje.minusDays(2), "Variável"),
                new Gasto(idUsuario1, idConta1, cat.get("Lazer"), "Cinema e jantar", new BigDecimal("218.00"), hoje.minusDays(1), "Variável")
        };
        List<Integer> novos = new ArrayList<>();
        for (Gasto g : gastos) {
            novos.add(gastoDAO.insert(g));
            System.out.println("  inserido: id=" + g.getIdGasto() + " " + g.getDescricao());
        }

        List<Gasto> todos = gastoDAO.getAll();
        System.out.println("\n  getAll() retornou " + todos.size() + " gasto(s), do mais recente ao mais antigo:");
        System.out.printf("  %-4s %-8s %-6s %-6s %-24s %12s %-12s %-9s%n", "ID", "USUARIO", "CONTA", "CATEG", "DESCRICAO", "VALOR", "DATA", "TIPO");
        for (Gasto g : todos) {
            System.out.printf("  %-4d %-8d %-6d %-6d %-24s %12s %-12s %-9s%s%n", g.getIdGasto(), g.getIdUsuario(),
                    g.getIdConta(), g.getIdCategoria(), g.getDescricao(), dinheiro(g.getValor()), g.getDtGasto(),
                    g.getTipo(), novos.contains(g.getIdGasto()) ? "  <- novo" : "");
        }
        conferir("getAll() contém os 5 gastos inseridos",
                todos.stream().map(Gasto::getIdGasto).toList().containsAll(novos));
        conferir("tipo normalizado para FIXO/VARIAVEL", todos.stream()
                .filter(g -> novos.contains(g.getIdGasto()))
                .allMatch(g -> "FIXO".equals(g.getTipo()) || "VARIAVEL".equals(g.getTipo())));
        boolean ordenado = true;
        for (int i = 1; i < todos.size(); i++) {
            ordenado &= !todos.get(i - 1).getDtGasto().isBefore(todos.get(i).getDtGasto());
        }
        conferir("getAll() ordenado do mais recente ao mais antigo", ordenado);
    }

    // -------------------------------------------------------------- Investimento
    private static void testarInvestimentos() throws DaoException {
        titulo("INVESTIMENTO - insert() x5 e getAll()");
        LocalDate hoje = LocalDate.now();

        Investimento cdb = new Investimento(idUsuario1, idConta1, "CDB Banco X 110% CDI", "CDB", new BigDecimal("5000.00"), hoje.minusDays(20));
        cdb.setInstituicao("Banco X");
        cdb.setTaxaRentabilidade(new BigDecimal("0.1250"));
        cdb.setDtVencimento(hoje.plusYears(2));

        Investimento tesouro = new Investimento(idUsuario1, idConta1, "Tesouro Selic 2029", "Tesouro", new BigDecimal("3000.00"), hoje.minusDays(15));
        tesouro.setInstituicao("Tesouro Direto");
        tesouro.setTaxaRentabilidade(new BigDecimal("0.1075"));
        tesouro.setDtVencimento(hoje.plusYears(3));

        Investimento acoes = new Investimento(idUsuario1, idConta1, "PETR4 - 100 ações", "Ações", new BigDecimal("3650.00"), hoje.minusDays(10));
        acoes.setInstituicao("Corretora Y"); // renda variável: sem taxa e sem vencimento (colunas opcionais)

        Investimento fii = new Investimento(idUsuario1, idConta1, "HGLG11 - 20 cotas", "FII", new BigDecimal("3200.00"), hoje.minusDays(5));
        fii.setInstituicao("Corretora Y");

        Investimento fundo = new Investimento(idUsuario1, idConta1, "Fundo DI Conservador", "Fundo", new BigDecimal("1500.00"), hoje.minusDays(1));
        fundo.setInstituicao("Banco X");
        fundo.setTaxaRentabilidade(new BigDecimal("0.1100"));

        Investimento[] investimentos = {cdb, tesouro, acoes, fii, fundo};
        List<Integer> novos = new ArrayList<>();
        for (Investimento i : investimentos) {
            novos.add(investimentoDAO.insert(i));
            System.out.println("  inserido: id=" + i.getIdInvestimento() + " " + i.getNomeInvestimento());
        }

        List<Investimento> todos = investimentoDAO.getAll();
        System.out.println("\n  getAll() retornou " + todos.size() + " investimento(s), do mais recente ao mais antigo:");
        System.out.printf("  %-4s %-6s %-24s %-9s %12s %8s %-12s %-12s %-8s%n", "ID", "CONTA", "NOME", "TIPO", "VALOR",
                "TAXA", "APLICACAO", "VENCIMENTO", "STATUS");
        for (Investimento i : todos) {
            System.out.printf("  %-4d %-6d %-24s %-9s %12s %8s %-12s %-12s %-8s%s%n", i.getIdInvestimento(), i.getIdConta(),
                    i.getNomeInvestimento(), i.getTipo(), dinheiro(i.getValorAplicado()),
                    i.getTaxaRentabilidade() == null ? "-" : i.getTaxaRentabilidade().toPlainString(), i.getDtAplicacao(),
                    i.getDtVencimento() == null ? "-" : i.getDtVencimento().toString(), i.getStatus(),
                    novos.contains(i.getIdInvestimento()) ? "  <- novo" : "");
        }
        conferir("getAll() contém os 5 investimentos inseridos",
                todos.stream().map(Investimento::getIdInvestimento).toList().containsAll(novos));
        conferir("colunas opcionais nulas (taxa/vencimento) recuperadas como null", todos.stream()
                .filter(i -> i.getIdInvestimento() == acoes.getIdInvestimento())
                .allMatch(i -> i.getTaxaRentabilidade() == null && i.getDtVencimento() == null));
    }

    // ---------------------------------------------------------------- Exceções
    /** Cada cenário provoca uma falha real e confere que o DAO a trata (DaoException com mensagem amigável). */
    private static void testarExcecoes() {
        titulo("TRATAMENTO DE EXCEÇÕES - falhas provocadas de propósito");

        if (emailUsuario1 != null) {
            esperarFalha("e-mail duplicado", 1, () ->
                    usuarioDAO.insert(new Usuario(0, "Duplicado", emailUsuario1, "hash")));
            esperarFalha("gasto com valor negativo (CHECK)", 2290, () ->
                    gastoDAO.insert(new Gasto(idUsuario1, idConta1, idCategoria1, "Valor inválido",
                            new BigDecimal("-10.00"), LocalDate.now(), "Fixo")));
            esperarFalha("gasto de usuário inexistente (FK)", 2291, () ->
                    gastoDAO.insert(new Gasto(999999999, idConta1, idCategoria1, "Usuário inexistente",
                            new BigDecimal("10.00"), LocalDate.now(), "Fixo")));
        } else {
            System.out.println("  (cenários que dependem de dados do teste foram pulados)");
        }

        esperarFalha("tabela inexistente", 942, () -> {
            try (Connection conn = ConnectionFactory.getConnection();
                 PreparedStatement ps = conn.prepareStatement("SELECT id FROM T_SF_TABELA_INEXISTENTE")) {
                ps.executeQuery();
            } catch (SQLException e) {
                throw DaoException.de("consultar a tabela T_SF_TABELA_INEXISTENTE", e);
            }
        });

        esperarFalha("banco fora do ar (porta sem Oracle)", 12541, () ->
                ConnectionFactory.getConnection("jdbc:oracle:thin:@//127.0.0.1:1/ORCL", "x", "x"));
    }

    // ----------------------------------------------------------------- Auxiliares
    @FunctionalInterface
    private interface Operacao {
        void executar() throws DaoException;
    }

    private static void esperarFalha(String cenario, int codigoEsperado, Operacao operacao) {
        try {
            operacao.executar();
            conferir(cenario + ": deveria ter falhado", false);
        } catch (DaoException e) {
            System.out.println("  [tratado] " + cenario + " -> " + e.getMessage());
            conferir(cenario + ": falha tratada (ORA-" + String.format("%05d", codigoEsperado) + ")",
                    e.getCodigoOracle() == codigoEsperado);
        }
    }

    private static void conferir(String descricao, boolean ok) {
        verificacoes++;
        if (!ok) {
            falhas++;
        }
        System.out.println("  [" + (ok ? "OK" : "FALHOU") + "] " + descricao);
    }

    private static String dinheiro(BigDecimal valor) {
        return valor.setScale(2, RoundingMode.HALF_UP).toPlainString();
    }

    private static void titulo(String texto) {
        System.out.println("\n===== " + texto + " =====");
    }
}
