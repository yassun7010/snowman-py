use clap::Args;
use convert_case::{Case, Casing};
use itertools::Itertools;
use snowq_generator::generate_modlue_init_py;
use tokio::io::AsyncWriteExt;

use crate::config::{get_pydantic_options, get_schema_output_dirpath};

#[derive(Debug, Args)]
pub struct SchemaSyncCommand {}

pub async fn run_schema_sync_command(
    _: SchemaSyncCommand,
) -> Result<(), Box<dyn std::error::Error>> {
    let config_file_path = snowq_config::find_path()?;
    let config = snowq_config::load_from_path(&config_file_path)?;
    let connection = snowq_connector::Connection::try_new_from_env()?;
    let pydantic_options = get_pydantic_options(&config);
    let schema_output_dirpath = &config_file_path
        .parent()
        .unwrap()
        .join(get_schema_output_dirpath(&config));

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

        let database_dir = &schema_output_dirpath.join(schema.database_name.to_case(Case::Snake));

        std::fs::create_dir_all(database_dir)?;

        tokio::fs::File::create(
            database_dir.join(format!("{}.py", schema.schema_name.to_case(Case::Snake))),
        )
        .await?
        .write_all(
            snowq_generator::generate_pydantic_schema(
                &schema.database_name,
                &schema.schema_name,
                &tables,
                &pydantic_options,
            )
            .as_bytes(),
        )
        .await?;

        Ok::<(), Box<dyn std::error::Error>>(())
    }))
    .await?;

    futures::future::try_join_all(
        schemas
            .iter()
            .into_group_map_by(|x| x.database_name.clone())
            .into_iter()
            .map(|(database_name, schemas)| async move {
                let schema_output_dirpath = &schema_output_dirpath;
                let database_dir = schema_output_dirpath.join(database_name.to_case(Case::Snake));
                let schema_names = schemas
                    .iter()
                    .map(|schema| schema.schema_name.to_case(Case::Snake))
                    .collect::<Vec<_>>();

                tokio::fs::File::create(database_dir.join("__init__.py"))
                    .await?
                    .write_all(
                        generate_modlue_init_py(
                            &schema_names
                                .iter()
                                .map(AsRef::as_ref)
                                .collect::<Vec<&str>>(),
                        )
                        .as_bytes(),
                    )
                    .await?;

                Ok::<(), Box<dyn std::error::Error>>(())
            }),
    )
    .await?;

    let database_names = &schemas
        .iter()
        .map(|schema| schema.database_name.to_case(Case::Snake))
        .collect::<Vec<_>>();

    tokio::fs::File::create(schema_output_dirpath.join("__init__.py"))
        .await?
        .write_all(
            generate_modlue_init_py(
                &database_names
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
