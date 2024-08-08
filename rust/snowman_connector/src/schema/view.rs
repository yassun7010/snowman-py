use super::column::Column;

pub struct View {
    pub database_name: String,
    pub schema_name: String,
    pub table_name: String,
    pub comment: Option<String>,
    pub columns: Vec<Column>,
}
