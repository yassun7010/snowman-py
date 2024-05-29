use crate::{
    schema::{Column, Table},
    Connection,
};

#[derive(Debug, Clone)]
pub struct SchemaInfomation {
    pub table_name: String,
    pub column_name: String,
    pub data_type: String,
    pub is_nullable: String,
}

pub async fn get_schema_infomations(
    connection: &Connection,
    database_name: &str,
    schema_name: &str,
) -> Result<Vec<Table>, crate::Error> {
    let rows = connection
        .execute(&format!(
            "
            SELECT
                t.table_catalog,
                t.table_schema,
                t.table_name,
                t.comment as table_comment,
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.comment as column_comment,
                c.column_default,
            FROM
                information_schema.tables t
            JOIN
                information_schema.columns c USING (table_schema, table_name)
            WHERE
                t.table_type = 'BASE TABLE'
                AND t.table_catalog = '{database_name}'
                AND t.table_schema = '{schema_name}'
            ORDER BY
                t.table_catalog,
                t.table_schema,
                t.table_name,
                c.ordinal_position
            "
        ))
        .await?;
    let mut tables = vec![];
    let mut table: Option<Table> = None;
    for row in rows {
        match table {
            Some(ref mut t) if t.table_name == row.get::<String>("table_name").unwrap() => {
                t.columns.push(Column {
                    column_name: row.get("column_name").unwrap(),
                    data_type: row.get("data_type").unwrap(),
                    is_nullable: row.get::<String>("is_nullable").unwrap() == "YES",
                    comment: row.get("column_comment").ok(),
                    default_value: row.get("column_default").ok(),
                });
            }
            _ => {
                if let Some(t) = table {
                    tables.push(t);
                }
                table = Some(Table {
                    database_name: row.get("table_catalog").unwrap(),
                    schema_name: row.get("table_schema").unwrap(),
                    table_name: row.get("table_name").unwrap(),
                    comment: row.get("table_comment").ok(),
                    columns: vec![Column {
                        column_name: row.get("column_name").unwrap(),
                        data_type: row.get("data_type").unwrap(),
                        is_nullable: row.get::<String>("is_nullable").unwrap() == "YES",
                        comment: row.get("column_comment").ok(),
                        default_value: row.get("column_default").ok(),
                    }],
                });
            }
        }
    }

    if let Some(t) = table {
        tables.push(t);
    }

    Ok(tables)
}
