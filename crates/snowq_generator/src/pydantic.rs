use convert_case::{Case, Casing};
use snowq_connector::schema::Table;

pub fn generate_pydantic_schema(table: &Table) -> String {
    let mut pydantic_schema = String::new();

    pydantic_schema.push_str(&format!(
        "class {}(pydantic.BaseModel):\n",
        table.table_name.to_case(Case::Pascal)
    ));
    for column in &table.columns {
        pydantic_schema.push_str(&format!(
            "    {}: snowq.datatype.{}\n",
            column.column_name.to_case(Case::Snake),
            column.data_type
        ));
        if let Some(comment) = column.comment.as_ref() {
            if !comment.is_empty() {
                pydantic_schema.push_str(&format!(r#"    """{}""""#, comment));
                pydantic_schema.push('\n');
            }
        }
        pydantic_schema.push('\n');
    }
    pydantic_schema
}
