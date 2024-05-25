pub fn generate_update_typeddict(
    database_name: &str,
    schema_name: &str,
    tables: &[Table],
    options: &PydanticOptions,
) -> String {
    let mut text = String::new();

    text.push_str("import typing\n");
    text.push_str("import snowq\n\n\n");

    text.push_str(
        &tables
            .iter()
            .map(|table| generate_pydantic_model(database_name, schema_name, table, options))
            .collect::<Vec<String>>()
            .join("\n\n"),
    );

    text
}
