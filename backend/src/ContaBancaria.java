public class ContaBancaria {

    private int idConta;
    private int idUsuario;
    private String nomeBanco;
    private String tipoConta;
    private String numeroConta;
    private boolean ativa;

    // Construtor padrão
    public ContaBancaria() {
    }

    // Construtor com parâmetros
    public ContaBancaria(int idConta, int idUsuario, String nomeBanco, String tipoConta, String numeroConta) {
        this.idConta = idConta;
        this.idUsuario = idUsuario;
        this.nomeBanco = nomeBanco;
        this.tipoConta = tipoConta;
        this.numeroConta = numeroConta;
        this.ativa = true;
    }

    // Getters e Setters
    public int getIdConta() {
        return idConta;
    }

    public void setIdConta(int idConta) {
        this.idConta = idConta;
    }

    public int getIdUsuario() {
        return idUsuario;
    }

    public void setIdUsuario(int idUsuario) {
        this.idUsuario = idUsuario;
    }

    public String getNomeBanco() {
        return nomeBanco;
    }

    public void setNomeBanco(String nomeBanco) {
        this.nomeBanco = nomeBanco;
    }

    public String getTipoConta() {
        return tipoConta;
    }

    public void setTipoConta(String tipoConta) {
        this.tipoConta = tipoConta;
    }

    public String getNumeroConta() {
        return numeroConta;
    }

    public void setNumeroConta(String numeroConta) {
        this.numeroConta = numeroConta;
    }

    public boolean isAtiva() {
        return ativa;
    }

    public void setAtiva(boolean ativa) {
        this.ativa = ativa;
    }

    // Métodos de negócio
    public void vincularConta() {
        System.out.println("Executando vincularConta(): vinculando a conta " + numeroConta + " do banco " + nomeBanco + " ao usuário.");
    }

    public void consultarSaldo() {
        System.out.println("Executando consultarSaldo(): consultando o saldo disponível na conta " + numeroConta + ".");
    }

    public void desativarConta() {
        System.out.println("Executando desativarConta(): desativando a conta " + numeroConta + ".");
    }
}
