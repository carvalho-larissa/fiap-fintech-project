import java.time.LocalDate;

public class Main {

    public static void main(String[] args) {

        System.out.println("===== USUARIO =====");
        Usuario usuario = new Usuario(1, "Larissa Gomes de Carvalho", "larissa@email.com", "senha123");
        usuario.cadastrarUsuario();
        usuario.validarEmail();
        usuario.atualizarPerfil();

        System.out.println("\n===== CONTA BANCARIA =====");
        ContaBancaria conta = new ContaBancaria(1, usuario.getIdUsuario(), "Itaú", "Corrente", "1234-5");
        conta.vincularConta();
        conta.consultarSaldo();
        conta.desativarConta();

        System.out.println("\n===== RECEITA =====");
        Receita receita = new Receita(1, usuario.getIdUsuario(), "Salário Empresa XPTO", 5800.00, "Salário");
        receita.registrarReceita();
        receita.editarReceita();
        receita.calcularTotalReceitas();

        System.out.println("\n===== GASTO =====");
        Gasto gasto = new Gasto(1, usuario.getIdUsuario(), "Aluguel apartamento", 1850.00, "Fixo");
        gasto.registrarGasto();
        gasto.categorizarGasto();
        gasto.calcularImpactoNoSaldo();

        System.out.println("\n===== DIVIDA =====");
        Divida divida = new Divida(1, usuario.getIdUsuario(), "Cartão de crédito Itaú", "Cartão", 1480.00, 6);
        divida.registrarParcelaAtraso();
        divida.calcularJuros();
        divida.exibirAlertaVencimento();

        System.out.println("\n===== META =====");
        Meta meta = new Meta(1, usuario.getIdUsuario(), "Viagem Europa", 12000.00, LocalDate.of(2025, 12, 31));
        meta.criarMeta();
        meta.registrarAporte();
        meta.calcularProgresso();
        meta.validarOrcamentoDisponivel();
    }
}