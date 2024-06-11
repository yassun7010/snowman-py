use crate::{
    config::{get_model_output_dirpath, get_pydantic_options, get_snowflake_connection},
    database::fetch_database_schemas,
    formatter::run_ruff_format_if_exists,
};

use anyhow::anyhow;
use itertools::Itertools;
use snowman_connector::query::DatabaseSchema;
use snowman_generator::ToPython;
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

    let insert_typeddict_options = snowman_generator::InsertTypedDictOptions::default();
    let update_typeddict_options = snowman_generator::UpdateTypedDictOptions::default();
    let pydantic_options = get_pydantic_options(&config);

    let output_dirpath = &config_source.as_ref().parent().unwrap().join(
        args.output_dir
            .unwrap_or_else(|| get_model_output_dirpath(&config)),
    );

    let schemas = fetch_database_schemas(&connection, &config).await?;

    if schemas.is_empty() {
        Err(anyhow!("No database schema found to generate models."))?;
    }

    for schema in &schemas {
        println!(
            "Generating models for {}.{}",
            schema.database_name, schema.schema_name
        );
    }

    // remove existing files
    schemas.iter().try_for_each(|schema| {
        let database_module_path = output_dirpath.join(schema.database_module());
        if database_module_path.exists() {
            std::fs::remove_dir_all(&database_module_path)?;
        }
        Ok::<_, anyhow::Error>(())
    })?;

    // generate models
    futures::future::try_join_all(schemas.iter().map(|schema| async {
        write_schema_py(
            &connection,
            output_dirpath,
            schema,
            &pydantic_options,
            &insert_typeddict_options,
            &update_typeddict_options,
        )
        .await
    }))
    .await?;

    futures::future::try_join_all(
        schemas
            .iter()
            .into_group_map_by(|x| x.database_module())
            .into_iter()
            .map(|(database_module, schemas)| async move {
                write_database_init_py(output_dirpath, &database_module, &schemas).await
            }),
    )
    .await?;

    run_ruff_format_if_exists(output_dirpath)?;

    eprintln!("✅ Models generated successfully");

    Ok(())
}

async fn write_schema_py(
    connection: &snowman_connector::Connection,
    output_dirpath: &std::path::Path,
    schema: &DatabaseSchema,
    pydantic_options: &snowman_generator::PydanticOptions,
    insert_typeddict_options: &snowman_generator::InsertTypedDictOptions,
    update_typeddict_options: &snowman_generator::UpdateTypedDictOptions,
) -> Result<(), anyhow::Error> {
    let src = snowman_generator::generate_schema_python_code(
        connection,
        schema,
        pydantic_options,
        insert_typeddict_options,
        update_typeddict_options,
    )
    .await?;

    let target_file = schema.schema_file_fullpath(output_dirpath);

    if let Some(parent_dir) = target_file.parent() {
        tokio::fs::create_dir_all(parent_dir).await?;
    }

    tokio::fs::File::create(target_file)
        .await?
        .write_all(src.as_bytes())
        .await?;

    Ok(())
}

async fn write_database_init_py(
    output_dirpath: &std::path::Path,
    database_module: &str,
    schemas: &[&DatabaseSchema],
) -> Result<(), anyhow::Error> {
    tokio::fs::File::create(output_dirpath.join(database_module).join("__init__.py"))
        .await?
        .write_all(
            snowman_generator::generate_database_init_python_code(schemas)
                .await?
                .as_bytes(),
        )
        .await?;

    Ok(())
}
