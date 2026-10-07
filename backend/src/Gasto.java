import java.math.BigDecimal;
import java.time.LocalDate;

public class Gasto {

    private int idGasto;
    private int idUsuario;
    private int idConta;
    private int idCategoria;
    private String descricao;
    private BigDecimal valor;
    private LocalDate dtGasto;
    private String tipo; // "FIXO" ou "VARIAVEL" (o DAO normaliza "Fixo", "Variável" etc.)
    private String comprovante;

    // Construtor padrão
    public Gasto() {
    }

    // Construtor com parâmetros
    public Gasto(int idGasto, int idUsuario, String descricao, BigDecimal valor, String tipo) {
        this.idGasto = idGasto;
        this.idUsuario = idUsuario;
        this.descricao = descricao;
        this.valor = valor;
        this.tipo = tipo;
        this.dtGasto = LocalDate.now();
    }

    // Construtor completo para cadastro (o id é gerado pelo banco)
    public Gasto(int idUsuario, int idConta, int idCategoria, String descricao, BigDecimal valor,
                 LocalDate dtGasto, String tipo) {
        this.idUsuario = idUsuario;
        this.idConta = idConta;
        this.idCategoria = idCategoria;
        this.descricao = descricao;
        this.valor = valor;
        this.dtGasto = dtGasto;
        this.tipo = tipo;
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

    public int getIdCategoria() {
        return idCategoria;
    }

    public void setIdCategoria(int idCategoria) {
        this.idCategoria = idCategoria;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public BigDecimal getValor() {
        return valor;
    }

    public void setValor(BigDecimal valor) {
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

    public String getComprovante() {
        return comprovante;
    }

    public void setComprovante(String comprovante) {
        this.comprovante = comprovante;
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
