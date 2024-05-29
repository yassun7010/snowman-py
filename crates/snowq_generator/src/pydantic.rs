use convert_case::{Case, Casing};
use snowq_connector::schema::Table;

use crate::{InsertTypedDictOptions, UpdateTypedDictOptions};

#[derive(Debug, Clone, Default)]
pub struct PydanticOptions {
    pub model_name_prefix: Option<String>,
    pub model_name_suffix: Option<String>,
}

impl PydanticOptions {
    pub fn make_class_name(&self, table_name: &str) -> String {
        let mut table_name = table_name.to_case(Case::Pascal);
        if let Some(prefix) = &self.model_name_prefix {
            table_name.insert_str(0, prefix);
        }
        if let Some(suffix) = &self.model_name_suffix {
            table_name.push_str(suffix);
        }
        table_name
    }
}

pub fn get_pydantic_modules() -> Vec<&'static str> {
    vec!["pydantic", "snowq"]
}

pub fn generate_pydantic_models(
    database_name: &str,
    schema_name: &str,
    tables: &[Table],
    pydantic_options: &PydanticOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
) -> String {
    tables
        .iter()
        .map(|table| {
            generate_pydantic_model(
                database_name,
                schema_name,
                table,
                pydantic_options,
                insert_typeddict_options,
                update_typeddict_options,
            )
        })
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_pydantic_model(
    database_name: &str,
    schema_name: &str,
    table: &Table,
    pydantic_options: &PydanticOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
) -> String {
    let mut pydantic_schema = String::new();

    pydantic_schema.push_str(&format!(
        "@snowq.table(\"{database_name}\", \"{schema_name}\", \"{}\")\n",
        table.table_name
    ));
    pydantic_schema.push_str(&format!(
        "class {}(pydantic.BaseModel, snowq.Table[\"{}\",\"{}\"]):\n",
        pydantic_options.make_class_name(&table.table_name),
        insert_typeddict_options.make_class_name(&table.table_name),
        update_typeddict_options.make_class_name(&table.table_name)
    ));
    if let Some(comment) = &table.comment {
        if !comment.is_empty() {
            pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
        }
    }
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
                pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
            }
        }
    }
    pydantic_schema
}
