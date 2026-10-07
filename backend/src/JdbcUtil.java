import java.sql.Date;
import java.time.LocalDate;

/** Conversões entre java.time.LocalDate e java.sql.Date, tolerantes a null (colunas opcionais). */
final class JdbcUtil {

    private JdbcUtil() {
    }

    static Date paraSql(LocalDate data) {
        return data == null ? null : Date.valueOf(data);
    }

    static LocalDate paraLocal(Date data) {
        return data == null ? null : data.toLocalDate();
    }
}
