use convert_case::{Case, Casing};
use snowman_connector::schema::Table;

use crate::{ModelOptions, ToPythonModule};

#[derive(Debug, Clone)]
pub struct ColumnAccessorOptions {
    pub model_name_prefix: Option<String>,
    pub model_name_suffix: Option<String>,
}

impl ColumnAccessorOptions {
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

impl Default for ColumnAccessorOptions {
    fn default() -> Self {
        ColumnAccessorOptions {
            model_name_prefix: Some("_".to_string()),
            model_name_suffix: Some("ColumnAccessor".to_string()),
        }
    }
}

pub fn get_column_accessor_modules() -> Vec<&'static str> {
    vec!["typing", "snowman", "dataclasses"]
}

pub fn generate_column_accessors(tables: &[Table], model_options: &ModelOptions) -> String {
    tables
        .iter()
        .map(|table| generate_column_accessor(table, model_options))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_column_accessor(table: &Table, model_options: &ModelOptions) -> String {
    let mut text = String::new();
    let schema_module_name = table.schema_module();
    let table_class_name = model_options
        .pydantic_options
        .make_class_name(&table.table_name);
    let accessor_class_name = model_options
        .column_accessor_options
        .make_class_name(&table.table_name);

    text.push_str(&format!(
        "@dataclasses.dataclass(init=False, frozen=True, eq=False, order=False)\nclass {accessor_class_name}:",
    ));

    if table.columns.is_empty() {
        return text + "\n    pass\n";
    }

    for column in &table.columns {
        let mut data_type = format!("snowman.datatype.{}", column.data_type);
        if column.is_nullable {
            data_type.push_str(" | None");
        }
        let column_name = column.column_name.to_case(Case::Snake);
        text.push_str(&format!(
            "\n    {column_name}: snowman.Column[\"{schema_module_name}.{table_class_name}\", typing.Literal[\"{column_name}\"], {data_type}]\n",
        ));
        if let Some(comment) = column.comment.as_ref() {
            if !comment.is_empty() {
                text.push_str(&format!(r#"    """{}""""#, comment));
                text.push('\n');
            }
        }
    }

    text
}
