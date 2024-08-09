use crate::{
    config::{get_model_output_dirpath, get_pydantic_options, get_snowflake_connection},
    database::fetch_database_schemas,
};

use anyhow::anyhow;
use itertools::Itertools;
use snowman_config::TableType;
use snowman_connector::query::{get_parameters, DatabaseSchema};
use snowman_generator::{formatter::run_ruff_format_if_exists, ToPython};
use snowman_generator::{ModelOptions, ToPythonModule};
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
    let model_options = ModelOptions {
        pydantic_options: get_pydantic_options(&config),
        ..Default::default()
    };

    let output_dirpath = &config_source.as_ref().parent().unwrap().join(
        args.output_dir
            .unwrap_or_else(|| get_model_output_dirpath(&config)),
    );

    let database_schemas = fetch_database_schemas(&connection, &config).await?;
    let parameters = get_parameters(&connection).await?;

    if database_schemas.is_empty() {
        Err(anyhow!("No database schema found to generate models."))?;
    }

    for database_schema in &database_schemas {
        println!(
            "Generating models for {}.{}",
            database_schema.database_name, database_schema.schema_name
        );
    }

    // remove existing files
    database_schemas.iter().try_for_each(|database_schema| {
        for filepath in [
            database_schema.schema_python_code_fullpath(output_dirpath),
            database_schema.schema_python_typehint_fullpath(output_dirpath),
        ] {
            if filepath.exists() {
                std::fs::remove_file(&filepath)?;
            }
        }

        Ok::<_, anyhow::Error>(())
    })?;

    // Generate __init__.py for each database module
    futures::future::try_join_all(
        database_schemas
            .iter()
            .into_group_map_by(|x| x.database_module())
            .into_iter()
            .map(|(database_module, database_schemas)| async move {
                write_database_init_py(output_dirpath, &database_module, &database_schemas).await
            }),
    )
    .await?;

    // Generate models
    futures::future::try_join_all(database_schemas.iter().map(|database_schema| async {
        write_schema_py(
            &connection,
            output_dirpath,
            database_schema,
            config.model.get_schema_table_types(
                &database_schema.database_name,
                &database_schema.schema_name,
            ),
            &model_options,
            &parameters,
        )
        .await
    }))
    .await?;

    run_ruff_format_if_exists(output_dirpath)?;

    eprintln!("✅ Models generated successfully");

    Ok(())
}

async fn write_schema_py(
    connection: &snowman_connector::Connection,
    output_dirpath: &std::path::Path,
    database_schema: &DatabaseSchema,
    table_types: &[TableType],
    model_options: &ModelOptions,
    params: &snowman_connector::Parameters,
) -> Result<(), anyhow::Error> {
    let infomation_schema = snowman_connector::query::get_infomation_schema(
        connection,
        &database_schema.database_name,
        &database_schema.schema_name,
        &table_types
            .iter()
            .map(|x| x.to_string())
            .collect::<Vec<_>>(),
    )
    .await?;

    tokio::fs::File::create(database_schema.schema_python_typehint_fullpath(output_dirpath))
        .await?
        .write_all(
            snowman_generator::generate_schema_python_typehint(
                &infomation_schema.tables,
                &infomation_schema.views,
                &model_options.column_accessor_options,
                &model_options.insert_typeddict_options,
                &model_options.update_typeddict_options,
            )
            .await?
            .as_bytes(),
        )
        .await?;

    tokio::fs::File::create(database_schema.schema_python_code_fullpath(output_dirpath))
        .await?
        .write_all(
            snowman_generator::generate_schema_python_code(
                &infomation_schema.tables,
                &infomation_schema.views,
                database_schema,
                model_options,
                params,
            )
            .await?
            .as_bytes(),
        )
        .await?;

    Ok(())
}

async fn write_database_init_py(
    output_dirpath: &std::path::Path,
    database_module: &str,
    schemas: &[&DatabaseSchema],
) -> Result<(), anyhow::Error> {
    let database_dirpath = output_dirpath.join(database_module);

    if !database_dirpath.exists() {
        tokio::fs::create_dir_all(&database_dirpath).await?;
    }

    tokio::fs::File::create(database_dirpath.join("__init__.py"))
        .await?
        .write_all(
            snowman_generator::generate_database_init_python_code(schemas)
                .await?
                .as_bytes(),
        )
        .await?;

    Ok(())
}
