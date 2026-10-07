import java.math.BigDecimal;
import java.time.LocalDate;

public class Investimento {

    private int idInvestimento;
    private int idUsuario;
    private int idConta;
    private String nomeInvestimento;
    private String tipo; // CDB, LCI, LCA, TESOURO, ACOES, FII, FUNDO, POUPANCA, CRIPTO, OUTROS
    private String instituicao;
    private BigDecimal valorAplicado;
    private BigDecimal taxaRentabilidade; // fração anual: 0.1250 = 12,5% a.a. (opcional)
    private LocalDate dtAplicacao;
    private LocalDate dtVencimento; // opcional
    private String status; // ATIVO, RESGATADO, VENCIDO

    // Construtor padrão
    public Investimento() {
    }

    // Construtor com parâmetros (o id é gerado pelo banco)
    public Investimento(int idUsuario, int idConta, String nomeInvestimento, String tipo, BigDecimal valorAplicado,
                        LocalDate dtAplicacao) {
        this.idUsuario = idUsuario;
        this.idConta = idConta;
        this.nomeInvestimento = nomeInvestimento;
        this.tipo = tipo;
        this.valorAplicado = valorAplicado;
        this.dtAplicacao = dtAplicacao;
        this.status = "ATIVO";
    }

    // Getters e Setters
    public int getIdInvestimento() {
        return idInvestimento;
    }

    public void setIdInvestimento(int idInvestimento) {
        this.idInvestimento = idInvestimento;
    }

    public int getIdUsuario() {
        return idUsuario;
    }

    public void setIdUsuario(int idUsuario) {
        this.idUsuario = idUsuario;
    }

    public int getIdConta() {
        return idConta;
    }

    public void setIdConta(int idConta) {
        this.idConta = idConta;
    }

    public String getNomeInvestimento() {
        return nomeInvestimento;
    }

    public void setNomeInvestimento(String nomeInvestimento) {
        this.nomeInvestimento = nomeInvestimento;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public String getInstituicao() {
        return instituicao;
    }

    public void setInstituicao(String instituicao) {
        this.instituicao = instituicao;
    }

    public BigDecimal getValorAplicado() {
        return valorAplicado;
    }

    public void setValorAplicado(BigDecimal valorAplicado) {
        this.valorAplicado = valorAplicado;
    }

    public BigDecimal getTaxaRentabilidade() {
        return taxaRentabilidade;
    }

    public void setTaxaRentabilidade(BigDecimal taxaRentabilidade) {
        this.taxaRentabilidade = taxaRentabilidade;
    }

    public LocalDate getDtAplicacao() {
        return dtAplicacao;
    }

    public void setDtAplicacao(LocalDate dtAplicacao) {
        this.dtAplicacao = dtAplicacao;
    }

    public LocalDate getDtVencimento() {
        return dtVencimento;
    }

    public void setDtVencimento(LocalDate dtVencimento) {
        this.dtVencimento = dtVencimento;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    // Métodos de negócio
    public void registrarInvestimento() {
        System.out.println("Executando registrarInvestimento(): registrando a aplicação '" + nomeInvestimento + "' no valor de R$ " + valorAplicado + ".");
    }

    public void calcularRendimentoEstimado() {
        System.out.println("Executando calcularRendimentoEstimado(): estimando o rendimento anual de '" + nomeInvestimento + "'.");
    }

    public void resgatarInvestimento() {
        System.out.println("Executando resgatarInvestimento(): resgatando o investimento '" + nomeInvestimento + "'.");
    }
}
