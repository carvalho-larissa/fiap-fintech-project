import java.time.LocalDate;

public class Meta {

    private int idMeta;
    private int idUsuario;
    private String nome;
    private double valorAlvo;
    private double valorAcumulado;
    private LocalDate prazo;
    private String status;
    private LocalDate dtCriacao;

    // Construtor padrão
    public Meta() {
    }

    // Construtor com parâmetros
    public Meta(int idMeta, int idUsuario, String nome, double valorAlvo, LocalDate prazo) {
        this.idMeta = idMeta;
        this.idUsuario = idUsuario;
        this.nome = nome;
        this.valorAlvo = valorAlvo;
        this.valorAcumulado = 0.0;
        this.prazo = prazo;
        this.status = "No ritmo";
        this.dtCriacao = LocalDate.now();
    }

    // Getters e Setters
    public int getIdMeta() {
        return idMeta;
    }

    public void setIdMeta(int idMeta) {
        this.idMeta = idMeta;
    }

    public int getIdUsuario() {
        return idUsuario;
    }

    public void setIdUsuario(int idUsuario) {
        this.idUsuario = idUsuario;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public double getValorAlvo() {
        return valorAlvo;
    }

    public void setValorAlvo(double valorAlvo) {
        this.valorAlvo = valorAlvo;
    }

    public double getValorAcumulado() {
        return valorAcumulado;
    }

    public void setValorAcumulado(double valorAcumulado) {
        this.valorAcumulado = valorAcumulado;
    }

    public LocalDate getPrazo() {
        return prazo;
    }

    public void setPrazo(LocalDate prazo) {
        this.prazo = prazo;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDate getDtCriacao() {
        return dtCriacao;
    }

    public void setDtCriacao(LocalDate dtCriacao) {
        this.dtCriacao = dtCriacao;
    }

    // Métodos de negócio
    public void criarMeta() {
        System.out.println("Executando criarMeta(): criando a meta '" + nome + "' com valor alvo de R$ " + valorAlvo + ".");
    }

    public void registrarAporte() {
        System.out.println("Executando registrarAporte(): registrando um novo aporte na meta '" + nome + "'.");
    }

    public void calcularProgresso() {
        System.out.println("Executando calcularProgresso(): calculando o percentual concluído da meta '" + nome + "'.");
    }

    public void validarOrcamentoDisponivel() {
        System.out.println("Executando validarOrcamentoDisponivel(): verificando se a meta '" + nome + "' é compatível com o orçamento do usuário.");
    }
}
