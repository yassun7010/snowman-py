use convert_case::{Case, Casing};
use snowq_connector::schema::Table;

#[derive(Debug, Clone, Default)]
pub struct PydanticOptions {
    pub model_name_suffix: Option<String>,
}

pub fn get_pydantic_modules() -> Vec<&'static str> {
    vec!["pydantic", "snowq"]
}

pub fn generate_pydantic_models(
    database_name: &str,
    schema_name: &str,
    tables: &[Table],
    options: &PydanticOptions,
) -> String {
    tables
        .iter()
        .map(|table| generate_pydantic_model(database_name, schema_name, table, options))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_pydantic_model(
    database_name: &str,
    schema_name: &str,
    table: &Table,
    options: &PydanticOptions,
) -> String {
    let mut pydantic_schema = String::new();
    let mut model_class_name = table.table_name.to_case(Case::Pascal);
    if let Some(suffix) = &options.model_name_suffix {
        model_class_name.push_str(suffix);
    }

    pydantic_schema.push_str(&format!(
        "@snowq.table(\"{database_name}\", \"{schema_name}\", \"{}\")\n",
        table.table_name
    ));
    pydantic_schema.push_str(&format!(
        "class {}(pydantic.BaseModel, snowq.Table):",
        model_class_name
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
