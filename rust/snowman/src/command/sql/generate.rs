use crate::{config::get_snowflake_connection, database::fetch_database_schemas};

use anyhow::anyhow;
use itertools::Itertools;
use snowman_config::TableType;
use snowman_connector::{query::DatabaseSchema, Connection};
use snowman_generator::ToSQL;
use tokio::io::AsyncWriteExt;

#[derive(clap::Args)]
pub struct Args {
    /// Output directory for generated models
    #[arg(long)]
    pub output_dir: Option<std::path::PathBuf>,
}

pub async fn run(args: Args) -> Result<(), anyhow::Error> {
    let config_source = snowman_config::find_path()?;
    let config = snowman_config::load_from_source(&config_source)?;
    let connection = get_snowflake_connection(&config)?;

    // defualt pwd
    let output_dirpath = &config_source.as_ref().parent().unwrap().join(
        args.output_dir
            .unwrap_or_else(|| std::env::current_dir().unwrap()),
    );

    let database_schemas = fetch_database_schemas(&connection, &config).await?;

    if database_schemas.is_empty() {
        Err(anyhow!("No database schema found to generate models."))?;
    }

    for database_schema in &database_schemas {
        println!(
            "Generating models for {}.{}",
            database_schema.database_name, database_schema.schema_name
        );
    }

    // generate models
    futures::future::try_join_all(database_schemas.iter().map(|database_schema| async {
        write_sql_tables(
            &connection,
            output_dirpath,
            database_schema,
            &config.model.table_types,
        )
        .await
    }))
    .await?;

    eprintln!("✅ Tables generated successfully");

    Ok(())
}

async fn write_sql_tables(
    connection: &Connection,
    output_dirpath: &std::path::Path,
    database_schema: &DatabaseSchema,
    table_types: &[TableType],
) -> Result<(), anyhow::Error> {
    let information_schema = snowman_connector::query::get_infomation_schema(
        connection,
        database_schema.database_name.as_str(),
        database_schema.schema_name.as_str(),
        table_types,
    )
    .await?;

    let src = information_schema
        .tables
        .iter()
        .map(snowman_generator::generate_sql_definition)
        .join("\n");

    let target_file = database_schema.schema_sql_file_fullpath(output_dirpath);

    if let Some(parent_dir) = target_file.parent() {
        tokio::fs::create_dir_all(parent_dir).await?;
    }

    tokio::fs::File::create(target_file)
        .await?
        .write_all(src.as_bytes())
        .await?;

    Ok(())
}
