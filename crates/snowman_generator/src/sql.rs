use itertools::Itertools;
use snowman_connector::schema::Table;

pub fn generate_sql_definition(table: &Table) -> String {
    let mut sql_definition = String::new();
    sql_definition.push_str(&format!(
        "CREATE TABLE {}.{}.{} (\n",
        table.database_name, table.schema_name, table.table_name
    ));

    sql_definition.push_str(
        &table
            .columns
            .iter()
            .map(|column| {
                let mut column_definition = "    ".to_string();
                column_definition
                    .push_str(&format!("{} {}", &column.column_name, &column.data_type));

                if !column.is_nullable {
                    column_definition.push_str(" NOT NULL");
                }
                if let Some(default_value) = &column.default_value {
                    column_definition.push_str(&format!(" DEFAULT {}", default_value));
                }
                if let Some(comment) = &column.comment {
                    column_definition.push_str(&format!(" COMMENT '{}'", comment));
                }

                column_definition
            })
            .join(",\n"),
    );
    sql_definition.push_str("\n)");

    if let Some(comment) = &table.comment {
        if !comment.is_empty() {
            sql_definition.push_str(&format!(" COMMENT '{}'", comment));
        }
    }

    sql_definition + ";\n"
}
