use crate::Connection;

pub struct DatabaseSchema {
    pub database_name: String,
    pub schema_name: String,
}

pub async fn get_schemas(connection: &Connection) -> Result<Vec<DatabaseSchema>, crate::Error> {
    let rows = connection
        .execute(
            "
            SELECT
                catalog_name as database_name,
                schema_name
            FROM
                information_schema.schemata
            ",
        )
        .await?;
    let mut tables = vec![];
    for row in rows {
        tables.push(DatabaseSchema {
            database_name: row.get("database_name").unwrap(),
            schema_name: row.get("schema_name").unwrap(),
        });
    }
    Ok(tables)
}
