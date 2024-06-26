use itertools::Itertools;
use snowman_connector::query::{get_databases, DatabaseSchema};

pub async fn fetch_database_schemas(
    connection: &snowman_connector::Connection,
    config: &snowman_config::Config,
) -> Result<Vec<DatabaseSchema>, snowman_connector::Error> {
    let schemas = futures::future::try_join_all(
        get_databases(connection)
            .await?
            .into_iter()
            .filter(|name| config.model.include_database(name))
            .unique()
            .map(|database_name| async {
                snowman_connector::query::get_schemas(connection, database_name).await
            }),
    )
    .await?
    .into_iter()
    .flatten()
    .filter(|schema| {
        config
            .model
            .include_database_schema(&schema.database_name, &schema.schema_name)
    })
    .collect::<Vec<_>>();

    Ok(schemas)
}
