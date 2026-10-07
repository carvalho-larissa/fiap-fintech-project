import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/** Acesso à tabela T_SF_USUARIO. A senha só é gravada (hash) e nunca é lida de volta (D-05). */
public class UsuarioDAO {

    private static final String INSERT =
            "INSERT INTO T_SF_USUARIO (nome, email, senha, avatar, dt_cadastro, ativo) VALUES (?, ?, ?, ?, ?, ?)";

    private static final String SELECT_ALL =
            "SELECT id_usuario, nome, email, avatar, dt_cadastro, ativo FROM T_SF_USUARIO ORDER BY id_usuario";

    /** Cadastra o usuário e devolve o id gerado pelo banco (também gravado no objeto). */
    public int insert(Usuario usuario) throws DaoException {
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(INSERT, new String[]{"id_usuario"})) {
            ps.setString(1, usuario.getNome());
            ps.setString(2, usuario.getEmail());
            ps.setString(3, usuario.getSenha());
            ps.setString(4, usuario.getAvatar());
            ps.setDate(5, JdbcUtil.paraSql(usuario.getDtCadastro() != null ? usuario.getDtCadastro() : LocalDate.now()));
            ps.setString(6, usuario.isAtivo() ? "S" : "N");
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    usuario.setIdUsuario(chaves.getInt(1));
                }
            }
            return usuario.getIdUsuario();
        } catch (SQLException e) {
            throw DaoException.de("inserir usuário", e);
        }
    }

    /** Recupera todos os usuários cadastrados. */
    public List<Usuario> getAll() throws DaoException {
        List<Usuario> usuarios = new ArrayList<>();
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(SELECT_ALL);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                Usuario u = new Usuario();
                u.setIdUsuario(rs.getInt("id_usuario"));
                u.setNome(rs.getString("nome"));
                u.setEmail(rs.getString("email"));
                u.setAvatar(rs.getString("avatar"));
                u.setDtCadastro(JdbcUtil.paraLocal(rs.getDate("dt_cadastro")));
                u.setAtivo("S".equals(rs.getString("ativo")));
                usuarios.add(u);
            }
        } catch (SQLException e) {
            throw DaoException.de("consultar usuários", e);
        }
        return usuarios;
    }
}
