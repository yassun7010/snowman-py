use std::path::Path;

use clap::Args;
use convert_case::{Case, Casing};
use tokio::io::AsyncWriteExt;

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

        let database_dir = Path::new("schema").join(schema.database_name.to_case(Case::Snake));
        std::fs::create_dir_all(&database_dir)?;
        let mut schema_file = tokio::fs::File::create(
            database_dir.join(format!("{}.py", schema.schema_name.to_case(Case::Snake))),
        )
        .await?;

        schema_file
            .write_all(
                snowq_generator::generate_pydantic_schema(
                    &schema.database_name,
                    &schema.schema_name,
                    &tables,
                )
                .as_bytes(),
            )
            .await?;

        Ok::<(), Box<dyn std::error::Error>>(())
    }))
    .await?;

    Ok(())
}
