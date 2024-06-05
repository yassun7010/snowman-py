use crate::Connection;

#[derive(Debug, Clone)]
pub struct DatabaseSchema {
    pub database_name: String,
    pub schema_name: String,
}

pub async fn get_schemas(
    connection: &Connection,
    database_names: &[&str],
) -> Result<Vec<DatabaseSchema>, crate::Error> {
    let mut db_schemas = vec![];
    for database_name in database_names {
        let schemas = get_schemas_by_database_name(connection, database_name).await?;
        db_schemas.extend(schemas);
    }
    Ok(db_schemas)
}

pub async fn get_schemas_by_database_name(
    connection: &Connection,
    database_name: &str,
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
