pub struct Column {
    pub column_name: String,
    pub data_type: String,
    pub is_nullable: bool,
    pub comment: Option<String>,
    pub default_value: Option<String>,
}
