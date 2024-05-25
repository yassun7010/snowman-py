use crate::config::{get_pydantic_options, get_python_models_output_dirpath};
use clap::Args;
use convert_case::{Case, Casing};
use itertools::Itertools;
use snowq_connector::query::DatabaseSchema;
use std::iter::Iterator;
use tokio::io::AsyncWriteExt;

#[derive(Debug, Args)]
pub struct SchemaSyncCommand {}

pub async fn run_schema_sync_command(
    _: SchemaSyncCommand,
) -> Result<(), Box<dyn std::error::Error>> {
    let config_file_path = snowq_config::find_path()?;
    let config = snowq_config::load_from_path(&config_file_path)?;
    let connection = snowq_connector::Connection::try_new_from_env()?;
    let update_typeddict_options = snowq_generator::UpdateTypedDictOptions::default();
    let pydantic_options = get_pydantic_options(&config);
    let output_dirpath = &config_file_path
        .parent()
        .unwrap()
        .join(get_python_models_output_dirpath(&config));

    let schemas = snowq_connector::query::get_schemas(&connection).await?;
    let database_module_names = &schemas
        .iter()
        .map(|schema| schema.database_name.to_case(Case::Snake))
        .collect::<Vec<_>>();
    let database_module_names = database_module_names
        .iter()
        .unique()
        .map(AsRef::as_ref)
        .collect::<Vec<_>>();

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

    futures::future::try_join_all(
        database_module_names
            .iter()
            .map(|database_name| async move {
                let database_module_path = output_dirpath.join(database_name);
                if database_module_path.exists() {
                    tokio::fs::remove_dir_all(&database_module_path).await?;
                }
                Ok::<(), Box<dyn std::error::Error>>(())
            }),
    )
    .await?;

    futures::future::try_join_all(schemas.iter().map(|schema| async {
        write_schema_py(
            &connection,
            output_dirpath,
            schema,
            &update_typeddict_options,
            &pydantic_options,
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

    write_output_init_py(output_dirpath, &database_module_names).await?;

    Ok(())
}

async fn write_schema_py(
    connection: &snowq_connector::Connection,
    output_dirpath: &std::path::Path,
    schema: &DatabaseSchema,
    update_typeddict_options: &snowq_generator::UpdateTypedDictOptions,
    pydantic_options: &snowq_generator::PydanticOptions,
) -> Result<(), Box<dyn std::error::Error>> {
    let tables = snowq_connector::query::get_schema_infomations(
        connection,
        &schema.database_name,
        &schema.schema_name,
    )
    .await?;

    let database_dir = &output_dirpath.join(schema.database_name.to_case(Case::Snake));

    std::fs::create_dir_all(database_dir)?;

    tokio::fs::File::create(
        database_dir.join(format!("{}.py", schema.schema_name.to_case(Case::Snake))),
    )
    .await?
    .write_all(
        (itertools::join(
            [
                snowq_generator::generate_import_modules(
                    &itertools::interleave(
                        snowq_generator::get_pydantic_modules(),
                        snowq_generator::get_update_typeddict_modules(),
                    )
                    .unique()
                    .collect::<Vec<&str>>(),
                ),
                snowq_generator::generate_update_typeddicts(
                    &schema.database_name,
                    &schema.schema_name,
                    &tables,
                    update_typeddict_options,
                ),
                snowq_generator::generate_pydantic_models(
                    &schema.database_name,
                    &schema.schema_name,
                    &tables,
                    pydantic_options,
                    update_typeddict_options,
                ),
            ],
            "\n",
        ))
        .as_bytes(),
    )
    .await?;

    Ok::<(), Box<dyn std::error::Error>>(())
}

async fn write_output_init_py(
    output_dirpath: &std::path::Path,
    database_module_names: &[&str],
) -> Result<(), Box<dyn std::error::Error>> {
    tokio::fs::File::create(output_dirpath.join("__init__.py"))
        .await?
        .write_all(
            snowq_generator::generate_modlue_init_py(
                &database_module_names
                    .iter()
                    .unique()
                    .map(AsRef::as_ref)
                    .collect::<Vec<&str>>(),
            )
            .as_bytes(),
        )
        .await?;

    Ok(())
}

async fn write_database_init_py(
    output_dirpath: &std::path::Path,
    database_name: &str,
    schemas: &[&DatabaseSchema],
) -> Result<(), Box<dyn std::error::Error>> {
    let output_dirpath = &output_dirpath;
    let database_dir = output_dirpath.join(database_name.to_case(Case::Snake));
    let schema_names = schemas
        .iter()
        .map(|schema| schema.schema_name.to_case(Case::Snake))
        .collect::<Vec<_>>();

    tokio::fs::File::create(database_dir.join("__init__.py"))
        .await?
        .write_all(
            snowq_generator::generate_modlue_init_py(
                &schema_names
                    .iter()
                    .map(AsRef::as_ref)
                    .collect::<Vec<&str>>(),
            )
            .as_bytes(),
        )
        .await?;

    Ok::<(), Box<dyn std::error::Error>>(())
}
