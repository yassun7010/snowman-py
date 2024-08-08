use convert_case::{Case, Casing};
use snowman_connector::schema::Table;

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

pub fn generate_column_accessors(tables: &[Table], options: &ColumnAccessorOptions) -> String {
    tables
        .iter()
        .map(|table| generate_column_accessor(table, options))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_column_accessor(table: &Table, options: &ColumnAccessorOptions) -> String {
    let mut text = String::new();

    text.push_str(&format!(
        "@dataclasses.dataclass(init=False, frozen=True, eq=False, order=False)\nclass {}:",
        options.make_class_name(&table.table_name)
    ));

    if table.columns.is_empty() {
        return text + "\n    pass\n";
    }

    for column in &table.columns {
        let mut data_type = format!("snowman.datatype.{}", column.data_type);
        if column.is_nullable {
            data_type.push_str(" | None");
        }
        text.push_str(&format!(
            "\n    {}: snowman.Column[{}]\n",
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
