use convert_case::{Case, Casing};
use snowman_connector::schema::Table;

use crate::ModelOptions;

#[derive(Debug, Clone)]
pub struct InsertTypedDictOptions {
    pub model_name_prefix: Option<String>,
    pub model_name_suffix: Option<String>,
}

impl InsertTypedDictOptions {
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

impl Default for InsertTypedDictOptions {
    fn default() -> Self {
        InsertTypedDictOptions {
            model_name_prefix: Some("_".to_string()),
            model_name_suffix: Some("InsertTypedDict".to_string()),
        }
    }
}

pub fn get_insert_typeddict_modules() -> Vec<&'static str> {
    vec!["typing", "snowman"]
}

pub fn generate_insert_typeddicts(tables: &[Table], model_options: &ModelOptions) -> String {
    tables
        .iter()
        .map(|table| generate_insert_typeddict(table, model_options))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_insert_typeddict(table: &Table, model_options: &ModelOptions) -> String {
    let mut text = String::new();

    text.push_str(&format!(
        "class {}(typing.TypedDict):",
        model_options
            .insert_typeddict_options
            .make_class_name(&table.table_name)
    ));

    if table.columns.is_empty() {
        return text + "\n    pass\n";
    }

    for column in &table.columns {
        let mut data_type = format!("snowman.datatype.{}", column.data_type);
        if column.is_nullable {
            data_type.push_str(" | None");
        }
        if column.default_value.is_some() || column.is_nullable {
            data_type = format!("typing.NotRequired[{}]", data_type);
        }
        text.push_str(&format!(
            "\n    {}: {}\n",
            column.column_name.to_case(Case::Snake),
            data_type
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
