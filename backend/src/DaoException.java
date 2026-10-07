import java.sql.SQLException;

/**
 * Exceção da camada de acesso a dados. Traduz erros do Oracle/JDBC em mensagens
 * compreensíveis (banco fora do ar, tabela inexistente, e-mail duplicado etc.).
 */
public class DaoException extends Exception {

    private static final long serialVersionUID = 1L;

    private final int codigoOracle;

    public DaoException(String mensagem) {
        super(mensagem);
        this.codigoOracle = 0;
    }

    public DaoException(String mensagem, Throwable causa) {
        super(mensagem, causa);
        this.codigoOracle = causa instanceof SQLException sql ? sql.getErrorCode() : 0;
    }

    public int getCodigoOracle() {
        return codigoOracle;
    }

    /** Converte uma SQLException na exceção do DAO, com mensagem amigável. */
    public static DaoException de(String operacao, SQLException e) {
        String motivo = switch (e.getErrorCode()) {
            case 942 -> "a tabela ou view não existe (ORA-00942). Verifique se o schema foi criado.";
            case 904 -> "coluna inexistente (ORA-00904). O SQL não confere com a tabela.";
            case 1 -> "registro duplicado (ORA-00001): já existe um valor igual em uma coluna única (ex.: e-mail).";
            case 1400 -> "campo obrigatório não informado (ORA-01400).";
            case 2290 -> "valor fora do permitido por uma regra da tabela (ORA-02290, CHECK).";
            case 2291 -> "referência inválida (ORA-02291): o usuário, a conta ou a categoria informada não existe.";
            case 2292 -> "registro em uso por outros registros (ORA-02292).";
            case 12899 -> "valor maior que o tamanho da coluna (ORA-12899).";
            case 1017 -> "usuário ou senha do banco inválidos (ORA-01017).";
            case 28000 -> "conta do banco bloqueada (ORA-28000).";
            case 12541, 17002 -> "banco de dados fora do ar ou inacessível (host, porta ou rede/VPN). " + e.getMessage();
            case 12514, 12505, 12154 -> "serviço/SID do Oracle não encontrado (ORA-" + e.getErrorCode() + ").";
            case 17868 -> "host do banco não encontrado (verifique o endereço e a rede).";
            default -> e.getMessage();
        };
        return new DaoException("Falha ao " + operacao + ": " + motivo, e);
    }
}
