use crate::Connection;

pub struct SchemaInfomation {
    pub table_name: String,
    pub column_name: String,
    pub data_type: String,
    pub is_nullable: String,
}

pub async fn get_schema_infomations(
    _connection: &Connection,
    _schema_name: &str,
) -> Result<Vec<SchemaInfomation>, Box<dyn std::error::Error>> {
    Ok(vec![])
}
