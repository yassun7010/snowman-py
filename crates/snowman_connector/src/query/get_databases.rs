use crate::Connection;

pub async fn get_databases(connection: &Connection) -> Result<Vec<String>, crate::Error> {
    let rows = connection.execute("SHOW DATABASES").await?;
    Ok(rows
        .iter()
        .map(|row| row.get::<String>("name").unwrap())
        .collect())
}
