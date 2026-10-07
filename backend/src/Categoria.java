public class Categoria {

    private int idCategoria;
    private String nome;
    private String tipo; // RECEITA ou GASTO

    // Construtor padrão
    public Categoria() {
    }

    // Construtor com parâmetros (o id é gerado pelo banco)
    public Categoria(String nome, String tipo) {
        this.nome = nome;
        this.tipo = tipo;
    }

    // Getters e Setters
    public int getIdCategoria() {
        return idCategoria;
    }

    public void setIdCategoria(int idCategoria) {
        this.idCategoria = idCategoria;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }
}
