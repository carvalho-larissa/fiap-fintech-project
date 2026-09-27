import java.time.LocalDate;

public class Usuario {

    private int idUsuario;
    private String nome;
    private String email;
    private String senha;
    private String avatar;
    private LocalDate dtCadastro;
    private boolean ativo;

    // Construtor padrão
    public Usuario() {
    }

    // Construtor com parâmetros
    public Usuario(int idUsuario, String nome, String email, String senha) {
        this.idUsuario = idUsuario;
        this.nome = nome;
        this.email = email;
        this.senha = senha;
        this.dtCadastro = LocalDate.now();
        this.ativo = true;
    }

    // Getters e Setters
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

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getSenha() {
        return senha;
    }

    public void setSenha(String senha) {
        this.senha = senha;
    }

    public String getAvatar() {
        return avatar;
    }

    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    public LocalDate getDtCadastro() {
        return dtCadastro;
    }

    public void setDtCadastro(LocalDate dtCadastro) {
        this.dtCadastro = dtCadastro;
    }

    public boolean isAtivo() {
        return ativo;
    }

    public void setAtivo(boolean ativo) {
        this.ativo = ativo;
    }

    // Métodos de negócio
    public void cadastrarUsuario() {
        System.out.println("Executando cadastrarUsuario(): salvando os dados de " + nome + " no banco de dados.");
    }

    public void validarEmail() {
        System.out.println("Executando validarEmail(): verificando se o e-mail " + email + " possui um formato válido.");
    }

    public void atualizarPerfil() {
        System.out.println("Executando atualizarPerfil(): atualizando as informações cadastrais do usuário " + nome + ".");
    }
}
