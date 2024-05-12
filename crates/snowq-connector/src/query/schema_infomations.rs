use crate::{
    schema::{Column, Table},
    Connection,
};

pub struct SchemaInfomation {
    pub table_name: String,
    pub column_name: String,
    pub data_type: String,
    pub is_nullable: String,
}

pub async fn get_schema_infomations(
    connection: &Connection,
) -> Result<Vec<Table>, Box<dyn std::error::Error>> {
    let rows = connection
        .execute(
            "
            SELECT
                t.table_catalog,
                t.table_schema,
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable,
            FROM
                information_schema.tables t
            JOIN
                information_schema.columns c USING (table_schema, table_name)
            WHERE
                t.table_type = 'BASE TABLE'
            ORDER BY
                t.table_catalog,
                t.table_schema,
                t.table_name,
                c.ordinal_position
            ",
        )
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
                    columns: vec![Column {
                        column_name: row.get("column_name").unwrap(),
                        data_type: row.get("data_type").unwrap(),
                        is_nullable: row.get::<String>("is_nullable").unwrap() == "YES",
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
