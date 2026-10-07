import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/** Acesso à tabela T_SF_CATEGORIA (pré-requisito das FKs de receita e gasto). */
public class CategoriaDAO {

    private static final String INSERT = "INSERT INTO T_SF_CATEGORIA (nome, tipo) VALUES (?, ?)";

    private static final String SELECT_ALL =
            "SELECT id_categoria, nome, tipo FROM T_SF_CATEGORIA ORDER BY id_categoria";

    public int insert(Categoria categoria) throws DaoException {
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(INSERT, new String[]{"id_categoria"})) {
            ps.setString(1, categoria.getNome());
            ps.setString(2, Dominios.normalizar(categoria.getTipo()));
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    categoria.setIdCategoria(chaves.getInt(1));
                }
            }
            return categoria.getIdCategoria();
        } catch (SQLException e) {
            throw DaoException.de("inserir categoria", e);
        }
    }

    public List<Categoria> getAll() throws DaoException {
        List<Categoria> categorias = new ArrayList<>();
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(SELECT_ALL);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                Categoria c = new Categoria();
                c.setIdCategoria(rs.getInt("id_categoria"));
                c.setNome(rs.getString("nome"));
                c.setTipo(rs.getString("tipo"));
                categorias.add(c);
            }
        } catch (SQLException e) {
            throw DaoException.de("consultar categorias", e);
        }
        return categorias;
    }
}
