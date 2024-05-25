use clap::Args;

#[derive(Debug, Args)]
pub struct SchemaSyncCommand {}

pub async fn run_schema_sync_command(
    _: SchemaSyncCommand,
) -> Result<(), Box<dyn std::error::Error>> {
    let connection = snowq_connector::Connection::try_new_from_env()?;

    let schemas = snowq_connector::query::get_schemas(&connection).await?;
    let exclude_schemas = [(
        Option::<String>::None,
        Some("INFORMATION_SCHEMA".to_string()),
    )];

    let schemas = schemas
        .into_iter()
        .filter(|schema| {
            !exclude_schemas.iter().any(|(database_name, schema_name)| {
                match (database_name, schema_name) {
                    (Some(database_name), Some(schema_name)) => {
                        schema.database_name == *database_name && schema.schema_name == *schema_name
                    }
                    (Some(database_name), None) => schema.database_name == *database_name,
                    (None, Some(schema_name)) => schema.schema_name == *schema_name,
                    (None, None) => false,
                }
            })
        })
        .collect::<Vec<_>>();

    futures::future::try_join_all(schemas.iter().map(|schema| async {
        let tables = snowq_connector::query::get_schema_infomations(
            &connection,
            &schema.database_name,
            &schema.schema_name,
        )
        .await?;

        for table in tables {
            println!("{}", snowq_generator::generate_pydantic_schema(&table));
        }

        Ok::<(), Box<dyn std::error::Error>>(())
    }))
    .await?;

    Ok(())
}
