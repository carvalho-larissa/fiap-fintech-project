import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/**
 * Abre conexões com o Oracle. A configuração é lida (nesta ordem) de:
 * 1. variáveis de ambiente DB_URL, DB_USER, DB_PASSWORD;
 * 2. arquivo db.properties (chaves url, user, password) na pasta atual ou em backend/.
 * Credenciais nunca ficam no código nem no git (ver db.properties.example).
 */
public final class ConnectionFactory {

    private static final String ARQUIVO = "db.properties";

    private ConnectionFactory() {
    }

    public static Connection getConnection() throws DaoException {
        Properties cfg = carregarConfiguracao();
        String url = cfg.getProperty("url");
        String user = cfg.getProperty("user");
        String password = cfg.getProperty("password");
        if (url == null || user == null || password == null) {
            throw new DaoException("Configuração do banco incompleta. Defina DB_URL, DB_USER e DB_PASSWORD "
                    + "ou preencha o arquivo " + ARQUIVO + " (modelo: " + ARQUIVO + ".example).");
        }
        return getConnection(url, user, password);
    }

    /** Abre uma conexão com parâmetros explícitos (útil para testar falhas de conexão). */
    public static Connection getConnection(String url, String user, String password) throws DaoException {
        try {
            return DriverManager.getConnection(url, user, password);
        } catch (SQLException e) {
            throw DaoException.de("conectar ao banco de dados", e);
        }
    }

    private static Properties carregarConfiguracao() throws DaoException {
        Properties cfg = new Properties();
        String url = System.getenv("DB_URL");
        if (url != null) {
            cfg.setProperty("url", url);
            cfg.setProperty("user", System.getenv().getOrDefault("DB_USER", ""));
            cfg.setProperty("password", System.getenv().getOrDefault("DB_PASSWORD", ""));
            return cfg;
        }
        for (Path caminho : new Path[]{Path.of(ARQUIVO), Path.of("backend", ARQUIVO)}) {
            if (Files.isRegularFile(caminho)) {
                try (InputStream in = Files.newInputStream(caminho)) {
                    cfg.load(in);
                    return cfg;
                } catch (IOException e) {
                    throw new DaoException("Não foi possível ler o arquivo " + caminho + ": " + e.getMessage(), e);
                }
            }
        }
        return cfg;
    }
}
