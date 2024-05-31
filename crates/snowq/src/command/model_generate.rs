use crate::config::{
    get_pydantic_options, get_schema_sync_output_dirpath, get_snowflake_connection,
};
use anyhow::Context;
use clap::Args;
use convert_case::{Case, Casing};
use itertools::Itertools;
use snowq_connector::query::DatabaseSchema;
use std::iter::Iterator;
use tokio::io::AsyncWriteExt;

#[derive(Debug, Args)]
pub struct ModelGenerateCommand {
    #[clap(long)]
    pub output_dir: Option<std::path::PathBuf>,
}

pub async fn run_model_generate_command(args: ModelGenerateCommand) -> Result<(), anyhow::Error> {
    let config_file_path = snowq_config::find_path()?;
    let config = snowq_config::load_from_path(&config_file_path)?;
    let connection = get_snowflake_connection(&config)?;
    let insert_typeddict_options = snowq_generator::InsertTypedDictOptions::default();
    let update_typeddict_options = snowq_generator::UpdateTypedDictOptions::default();
    let pydantic_options = get_pydantic_options(&config);
    let output_dirpath = &config_file_path.parent().unwrap().join(
        args.output_dir
            .unwrap_or_else(|| get_schema_sync_output_dirpath(&config)),
    );

    let schemas = snowq_connector::query::get_schemas(&connection)
        .await
        .with_context(|| "Failed to retrieve Snowflake Information Schema.")?;

    let database_module_names = &schemas
        .iter()
        .map(|schema| schema.database_name.to_case(Case::Snake))
        .collect::<Vec<_>>();
    let database_module_names = database_module_names
        .iter()
        .unique()
        .map(AsRef::as_ref)
        .collect::<Vec<&str>>();

    let exclude_schemas = [(
        Option::<String>::None,
        Some("INFORMATION_SCHEMA".to_string()),
    )];

    // exclude schemasa
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

    // remove existing files
    database_module_names.iter().try_for_each(|database_name| {
        let database_module_path = output_dirpath.join(database_name);
        if database_module_path.exists() {
            std::fs::remove_dir_all(&database_module_path)?;
        }
        Ok::<_, anyhow::Error>(())
    })?;

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
            .into_group_map_by(|x| x.database_name.clone())
            .into_iter()
            .map(|(database_name, schemas)| async move {
                write_database_init_py(output_dirpath, &database_name, &schemas).await
            }),
    )
    .await?;

    // write_output_init_py(output_dirpath, &database_module_names).await?;

    run_ruff_format_if_exists(output_dirpath);

    Ok(())
}

async fn write_schema_py(
    connection: &snowq_connector::Connection,
    output_dirpath: &std::path::Path,
    schema: &DatabaseSchema,
    pydantic_options: &snowq_generator::PydanticOptions,
    insert_typeddict_options: &snowq_generator::InsertTypedDictOptions,
    update_typeddict_options: &snowq_generator::UpdateTypedDictOptions,
) -> Result<(), anyhow::Error> {
    let tables = snowq_connector::query::get_schema_infomations(
        connection,
        &schema.database_name,
        &schema.schema_name,
    )
    .await?;

    let src = if tables.is_empty() {
        snowq_generator::generate_module_docs().to_string()
    } else {
        itertools::join(
            [
                snowq_generator::generate_module_docs(),
                &snowq_generator::generate_import_modules(
                    &itertools::chain!(
                        snowq_generator::get_insert_typeddict_modules(),
                        snowq_generator::get_update_typeddict_modules(),
                        snowq_generator::get_pydantic_modules(),
                    )
                    .unique()
                    .collect::<Vec<&str>>(),
                ),
                &snowq_generator::generate_type_checking(&itertools::join(
                    [
                        &snowq_generator::generate_insert_typeddicts(
                            &schema.database_name,
                            &schema.schema_name,
                            &tables,
                            insert_typeddict_options,
                        ),
                        &snowq_generator::generate_update_typeddicts(
                            &schema.database_name,
                            &schema.schema_name,
                            &tables,
                            update_typeddict_options,
                        ),
                    ],
                    "\n",
                )),
                &snowq_generator::generate_pydantic_models(
                    &schema.database_name,
                    &schema.schema_name,
                    &tables,
                    pydantic_options,
                    insert_typeddict_options,
                    update_typeddict_options,
                ),
            ],
            "\n",
        )
    };

    let database_dir = &output_dirpath.join(schema.database_name.to_case(Case::Snake));

    std::fs::create_dir_all(database_dir)?;

    tokio::fs::File::create(
        database_dir.join(format!("{}.py", schema.schema_name.to_case(Case::Snake))),
    )
    .await?
    .write_all(src.as_bytes())
    .await?;

    Ok(())
}

async fn write_database_init_py(
    output_dirpath: &std::path::Path,
    database_name: &str,
    schemas: &[&DatabaseSchema],
) -> Result<(), anyhow::Error> {
    let output_dirpath = &output_dirpath;
    let database_dir = output_dirpath.join(database_name.to_case(Case::Snake));
    let schema_names = schemas
        .iter()
        .map(|schema| schema.schema_name.to_case(Case::Snake))
        .collect::<Vec<_>>();

    tokio::fs::File::create(database_dir.join("__init__.py"))
        .await?
        .write_all(
            itertools::join(
                [
                    snowq_generator::generate_module_docs(),
                    &snowq_generator::generate_modlue_init_py(
                        &schema_names
                            .iter()
                            .map(AsRef::as_ref)
                            .collect::<Vec<&str>>(),
                    ),
                ],
                "\n",
            )
            .as_bytes(),
        )
        .await?;

    Ok(())
}

fn run_ruff_format_if_exists(output_dirpath: &std::path::Path) {
    // if ruff command found in local machine, run it on output_dirpath
    match std::process::Command::new("ruff")
        .arg("format")
        .arg(output_dirpath)
        .status()
    {
        Ok(status) => {
            if !status.success() {
                eprintln!("ruff command failed");
            }
        }
        Err(err) => {
            if err.kind() == std::io::ErrorKind::NotFound {
                return;
            }
            eprintln!("ruff command not found: {}", err);
        }
    }
}
