import java.time.LocalDate;

public class Gasto {

    private int idGasto;
    private int idUsuario;
    private int idConta;
    private String descricao;
    private double valor;
    private LocalDate dtGasto;
    private String tipo; // "Fixo" ou "Variavel"

    // Construtor padrão
    public Gasto() {
    }

    // Construtor com parâmetros
    public Gasto(int idGasto, int idUsuario, String descricao, double valor, String tipo) {
        this.idGasto = idGasto;
        this.idUsuario = idUsuario;
        this.descricao = descricao;
        this.valor = valor;
        this.tipo = tipo;
        this.dtGasto = LocalDate.now();
    }

    // Getters e Setters
    public int getIdGasto() {
        return idGasto;
    }

    public void setIdGasto(int idGasto) {
        this.idGasto = idGasto;
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

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public double getValor() {
        return valor;
    }

    public void setValor(double valor) {
        this.valor = valor;
    }

    public LocalDate getDtGasto() {
        return dtGasto;
    }

    public void setDtGasto(LocalDate dtGasto) {
        this.dtGasto = dtGasto;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    // Métodos de negócio
    public void registrarGasto() {
        System.out.println("Executando registrarGasto(): registrando o gasto '" + descricao + "' no valor de R$ " + valor + ".");
    }

    public void categorizarGasto() {
        System.out.println("Executando categorizarGasto(): classificando o gasto '" + descricao + "' como " + tipo + ".");
    }

    public void calcularImpactoNoSaldo() {
        System.out.println("Executando calcularImpactoNoSaldo(): calculando o impacto do gasto '" + descricao + "' no saldo final do usuário.");
    }
}
