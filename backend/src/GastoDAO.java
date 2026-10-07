import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/** Acesso à tabela T_SF_GASTO. */
public class GastoDAO {

    private static final String INSERT =
            "INSERT INTO T_SF_GASTO (id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante) "
                    + "VALUES (?, ?, ?, ?, ?, ?, ?, ?)";

    // Mais recente primeiro; empate de data desempatado pelo id (D-08)
    private static final String SELECT_ALL =
            "SELECT id_gasto, id_usuario, id_conta, id_categoria, descricao, valor, dt_gasto, tipo, comprovante "
                    + "FROM T_SF_GASTO ORDER BY dt_gasto DESC, id_gasto DESC";

    public int insert(Gasto gasto) throws DaoException {
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(INSERT, new String[]{"id_gasto"})) {
            ps.setInt(1, gasto.getIdUsuario());
            ps.setInt(2, gasto.getIdConta());
            ps.setInt(3, gasto.getIdCategoria());
            ps.setString(4, gasto.getDescricao());
            ps.setBigDecimal(5, gasto.getValor());
            ps.setDate(6, JdbcUtil.paraSql(gasto.getDtGasto() != null ? gasto.getDtGasto() : LocalDate.now()));
            ps.setString(7, Dominios.normalizar(gasto.getTipo()));
            ps.setString(8, gasto.getComprovante());
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    gasto.setIdGasto(chaves.getInt(1));
                }
            }
            return gasto.getIdGasto();
        } catch (SQLException e) {
            throw DaoException.de("inserir gasto", e);
        }
    }

    public List<Gasto> getAll() throws DaoException {
        List<Gasto> gastos = new ArrayList<>();
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(SELECT_ALL);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                Gasto g = new Gasto();
                g.setIdGasto(rs.getInt("id_gasto"));
                g.setIdUsuario(rs.getInt("id_usuario"));
                g.setIdConta(rs.getInt("id_conta"));
                g.setIdCategoria(rs.getInt("id_categoria"));
                g.setDescricao(rs.getString("descricao"));
                g.setValor(rs.getBigDecimal("valor"));
                g.setDtGasto(JdbcUtil.paraLocal(rs.getDate("dt_gasto")));
                g.setTipo(rs.getString("tipo"));
                g.setComprovante(rs.getString("comprovante"));
                gastos.add(g);
            }
        } catch (SQLException e) {
            throw DaoException.de("consultar gastos", e);
        }
        return gastos;
    }
}
