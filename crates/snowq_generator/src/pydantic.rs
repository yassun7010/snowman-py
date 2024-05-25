use convert_case::{Case, Casing};
use snowq_connector::schema::Table;

pub fn generate_pydantic_schema(
    database_name: &str,
    schema_name: &str,
    tables: &[Table],
) -> String {
    let mut text = String::new();

    text.push_str("import pydantic\n");
    text.push_str("import snowq\n\n\n");

    text.push_str(
        &tables
            .iter()
            .map(|table| generate_pydantic_table(database_name, schema_name, table))
            .collect::<Vec<String>>()
            .join("\n\n"),
    );

    text
}

pub fn generate_pydantic_table(database_name: &str, schema_name: &str, table: &Table) -> String {
    let mut pydantic_schema = String::new();

    pydantic_schema.push_str(&format!(
        "@snowq.table(\"{database_name}\", \"{schema_name}\", \"{}\")\n",
        table.table_name
    ));
    pydantic_schema.push_str(&format!(
        "class {}(pydantic.BaseModel, snowq.Table):",
        table.table_name.to_case(Case::Pascal)
    ));
    for column in &table.columns {
        let mut data_type = column.data_type.clone();
        if column.is_nullable {
            data_type.push_str(" | None");
        }
        pydantic_schema.push_str(&format!(
            "\n    {}: snowq.datatype.{}\n",
            column.column_name.to_case(Case::Snake),
            data_type
        ));
        if let Some(comment) = column.comment.as_ref() {
            if !comment.is_empty() {
                pydantic_schema.push_str(&format!(r#"    """{}""""#, comment));
                pydantic_schema.push('\n');
            }
        }
    }
    pydantic_schema
}
