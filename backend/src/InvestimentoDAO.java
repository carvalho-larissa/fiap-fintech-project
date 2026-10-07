import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/** Acesso à tabela T_SF_INVESTIMENTO. */
public class InvestimentoDAO {

    private static final String INSERT =
            "INSERT INTO T_SF_INVESTIMENTO (id_usuario, id_conta, nm_investimento, tipo, instituicao, vl_aplicado, "
                    + "tx_rentabilidade, dt_aplicacao, dt_vencimento, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

    // Mais recente primeiro; empate de data desempatado pelo id (D-08)
    private static final String SELECT_ALL =
            "SELECT id_investimento, id_usuario, id_conta, nm_investimento, tipo, instituicao, vl_aplicado, "
                    + "tx_rentabilidade, dt_aplicacao, dt_vencimento, status "
                    + "FROM T_SF_INVESTIMENTO ORDER BY dt_aplicacao DESC, id_investimento DESC";

    public int insert(Investimento investimento) throws DaoException {
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(INSERT, new String[]{"id_investimento"})) {
            ps.setInt(1, investimento.getIdUsuario());
            ps.setInt(2, investimento.getIdConta());
            ps.setString(3, investimento.getNomeInvestimento());
            ps.setString(4, Dominios.normalizar(investimento.getTipo()));
            ps.setString(5, investimento.getInstituicao());
            ps.setBigDecimal(6, investimento.getValorAplicado());
            ps.setBigDecimal(7, investimento.getTaxaRentabilidade());
            ps.setDate(8, JdbcUtil.paraSql(investimento.getDtAplicacao() != null ? investimento.getDtAplicacao() : LocalDate.now()));
            ps.setDate(9, JdbcUtil.paraSql(investimento.getDtVencimento()));
            ps.setString(10, investimento.getStatus() != null ? Dominios.normalizar(investimento.getStatus()) : "ATIVO");
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    investimento.setIdInvestimento(chaves.getInt(1));
                }
            }
            return investimento.getIdInvestimento();
        } catch (SQLException e) {
            throw DaoException.de("inserir investimento", e);
        }
    }

    public List<Investimento> getAll() throws DaoException {
        List<Investimento> investimentos = new ArrayList<>();
        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(SELECT_ALL);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                Investimento i = new Investimento();
                i.setIdInvestimento(rs.getInt("id_investimento"));
                i.setIdUsuario(rs.getInt("id_usuario"));
                i.setIdConta(rs.getInt("id_conta"));
                i.setNomeInvestimento(rs.getString("nm_investimento"));
                i.setTipo(rs.getString("tipo"));
                i.setInstituicao(rs.getString("instituicao"));
                i.setValorAplicado(rs.getBigDecimal("vl_aplicado"));
                i.setTaxaRentabilidade(rs.getBigDecimal("tx_rentabilidade"));
                i.setDtAplicacao(JdbcUtil.paraLocal(rs.getDate("dt_aplicacao")));
                i.setDtVencimento(JdbcUtil.paraLocal(rs.getDate("dt_vencimento")));
                i.setStatus(rs.getString("status"));
                investimentos.add(i);
            }
        } catch (SQLException e) {
            throw DaoException.de("consultar investimentos", e);
        }
        return investimentos;
    }
}
