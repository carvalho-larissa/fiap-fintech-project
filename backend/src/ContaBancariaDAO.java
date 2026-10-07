import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/** Acesso à tabela T_SF_CONTA_BANCARIA (pré-requisito das FKs de gasto e investimento). */
public class ContaBancariaDAO {

    private static final String INSERT =
            "INSERT INTO T_SF_CONTA_BANCARIA (id_usuario, nm_banco, tipo_conta, nr_conta, ativa) VALUES (?, ?, ?, ?, ?)";

    private static final String SELECT_ALL =
            "SELECT id_conta, id_usuario, nm_banco, tipo_conta, nr_conta, ativa FROM T_SF_CONTA_BANCARIA ORDER BY id_conta";

    public int insert(ContaBancaria conta) throws DaoException {
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(INSERT, new String[]{"id_conta"})) {
            ps.setInt(1, conta.getIdUsuario());
            ps.setString(2, conta.getNomeBanco());
            ps.setString(3, Dominios.normalizar(conta.getTipoConta()));
            ps.setString(4, conta.getNumeroConta());
            ps.setString(5, conta.isAtiva() ? "S" : "N");
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    conta.setIdConta(chaves.getInt(1));
                }
            }
            return conta.getIdConta();
        } catch (SQLException e) {
            throw DaoException.de("inserir conta bancária", e);
        }
    }

    public List<ContaBancaria> getAll() throws DaoException {
        List<ContaBancaria> contas = new ArrayList<>();
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(SELECT_ALL);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                ContaBancaria c = new ContaBancaria();
                c.setIdConta(rs.getInt("id_conta"));
                c.setIdUsuario(rs.getInt("id_usuario"));
                c.setNomeBanco(rs.getString("nm_banco"));
                c.setTipoConta(rs.getString("tipo_conta"));
                c.setNumeroConta(rs.getString("nr_conta"));
                c.setAtiva("S".equals(rs.getString("ativa")));
                contas.add(c);
            }
        } catch (SQLException e) {
            throw DaoException.de("consultar contas bancárias", e);
        }
        return contas;
    }
}
