import java.time.LocalDate;

public class Receita {

    private int idReceita;
    private int idUsuario;
    private int idConta;
    private String descricao;
    private double valor;
    private LocalDate dtRecebimento;
    private String origem;
    private String recorrencia;

    // Construtor padrão
    public Receita() {
    }

    // Construtor com parâmetros
    public Receita(int idReceita, int idUsuario, String descricao, double valor, String origem) {
        this.idReceita = idReceita;
        this.idUsuario = idUsuario;
        this.descricao = descricao;
        this.valor = valor;
        this.origem = origem;
        this.dtRecebimento = LocalDate.now();
    }

    // Getters e Setters
    public int getIdReceita() {
        return idReceita;
    }

    public void setIdReceita(int idReceita) {
        this.idReceita = idReceita;
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

    public LocalDate getDtRecebimento() {
        return dtRecebimento;
    }

    public void setDtRecebimento(LocalDate dtRecebimento) {
        this.dtRecebimento = dtRecebimento;
    }

    public String getOrigem() {
        return origem;
    }

    public void setOrigem(String origem) {
        this.origem = origem;
    }

    public String getRecorrencia() {
        return recorrencia;
    }

    public void setRecorrencia(String recorrencia) {
        this.recorrencia = recorrencia;
    }

    // Métodos de negócio
    public void registrarReceita() {
        System.out.println("Executando registrarReceita(): registrando a receita '" + descricao + "' no valor de R$ " + valor + ".");
    }

    public void editarReceita() {
        System.out.println("Executando editarReceita(): editando os dados da receita '" + descricao + "'.");
    }

    public void calcularTotalReceitas() {
        System.out.println("Executando calcularTotalReceitas(): somando todas as receitas registradas pelo usuário no período.");
    }
}
