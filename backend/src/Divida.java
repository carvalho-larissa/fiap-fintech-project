import java.time.LocalDate;

public class Divida {

    private int idDivida;
    private int idUsuario;
    private String descricao;
    private String tipo;
    private double valorTotal;
    private double saldoDevedor;
    private int totalParcelas;
    private double taxaJurosMensal;
    private String status;
    private LocalDate dtInicio;

    // Construtor padrão
    public Divida() {
    }

    // Construtor com parâmetros
    public Divida(int idDivida, int idUsuario, String descricao, String tipo, double valorTotal, int totalParcelas) {
        this.idDivida = idDivida;
        this.idUsuario = idUsuario;
        this.descricao = descricao;
        this.tipo = tipo;
        this.valorTotal = valorTotal;
        this.saldoDevedor = valorTotal;
        this.totalParcelas = totalParcelas;
        this.status = "Em dia";
        this.dtInicio = LocalDate.now();
    }

    // Getters e Setters
    public int getIdDivida() {
        return idDivida;
    }

    public void setIdDivida(int idDivida) {
        this.idDivida = idDivida;
    }

    public int getIdUsuario() {
        return idUsuario;
    }

    public void setIdUsuario(int idUsuario) {
        this.idUsuario = idUsuario;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public double getValorTotal() {
        return valorTotal;
    }

    public void setValorTotal(double valorTotal) {
        this.valorTotal = valorTotal;
    }

    public double getSaldoDevedor() {
        return saldoDevedor;
    }

    public void setSaldoDevedor(double saldoDevedor) {
        this.saldoDevedor = saldoDevedor;
    }

    public int getTotalParcelas() {
        return totalParcelas;
    }

    public void setTotalParcelas(int totalParcelas) {
        this.totalParcelas = totalParcelas;
    }

    public double getTaxaJurosMensal() {
        return taxaJurosMensal;
    }

    public void setTaxaJurosMensal(double taxaJurosMensal) {
        this.taxaJurosMensal = taxaJurosMensal;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDate getDtInicio() {
        return dtInicio;
    }

    public void setDtInicio(LocalDate dtInicio) {
        this.dtInicio = dtInicio;
    }

    // Métodos de negócio
    public void registrarParcelaAtraso() {
        System.out.println("Executando registrarParcelaAtraso(): registrando atraso na dívida '" + descricao + "'.");
    }

    public void calcularJuros() {
        System.out.println("Executando calcularJuros(): calculando os juros do mês sobre o saldo devedor da dívida '" + descricao + "'.");
    }

    public void exibirAlertaVencimento() {
        System.out.println("Executando exibirAlertaVencimento(): exibindo alerta visual de vencimento próximo para a dívida '" + descricao + "'.");
    }
}
