use crate::Connection;

#[derive(Debug, Clone)]
pub struct DatabaseSchema {
    pub database_name: String,
    pub schema_name: String,
}

pub async fn get_schemas(
    connection: &Connection,
    database_name: String,
) -> Result<Vec<DatabaseSchema>, crate::Error> {
    let rows = connection
        .execute(&format!(
            "
            SELECT
                catalog_name as database_name,
                schema_name
            FROM
                {}.information_schema.schemata
            ",
            database_name
        ))
        .await?;
    let mut db_schemas = vec![];
    for row in rows {
        db_schemas.push(DatabaseSchema {
            database_name: row.get("database_name").unwrap(),
            schema_name: row.get("schema_name").unwrap(),
        });
    }
    Ok(db_schemas)
}
