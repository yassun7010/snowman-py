use super::column::Column;

pub struct Table {
    pub table_type: String,
    pub database_name: String,
    pub schema_name: String,
    pub table_name: String,
    pub comment: Option<String>,
    pub columns: Vec<Column>,
}
