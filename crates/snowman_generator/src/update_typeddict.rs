use convert_case::{Case, Casing};
use snowman_connector::schema::Table;

#[derive(Debug, Clone)]
pub struct UpdateTypedDictOptions {
    pub model_name_prefix: Option<String>,
    pub model_name_suffix: Option<String>,
}

impl UpdateTypedDictOptions {
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

impl Default for UpdateTypedDictOptions {
    fn default() -> Self {
        UpdateTypedDictOptions {
            model_name_prefix: Some("_".to_string()),
            model_name_suffix: Some("UpdateTypedDict".to_string()),
        }
    }
}

pub fn get_update_typeddict_modules() -> Vec<&'static str> {
    vec!["typing", "snowman"]
}

pub fn generate_update_typeddicts(
    database_name: &str,
    schema_name: &str,
    tables: &[Table],
    options: &UpdateTypedDictOptions,
) -> String {
    tables
        .iter()
        .map(|table| generate_update_typeddict(database_name, schema_name, table, options))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_update_typeddict(
    _database_name: &str,
    _schema_name: &str,
    table: &Table,
    options: &UpdateTypedDictOptions,
) -> String {
    let mut text = String::new();

    text.push_str(&format!(
        "class {}(typing.TypedDict):",
        options.make_class_name(&table.table_name)
    ));
    for column in &table.columns {
        let mut data_type = format!("snowman.datatype.{}", column.data_type);
        if column.is_nullable {
            data_type.push_str(" | None");
        }
        text.push_str(&format!(
            "\n    {}: typing.NotRequired[{}]\n",
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
