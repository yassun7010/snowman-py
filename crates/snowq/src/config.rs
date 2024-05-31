use snowq_config::{Config, ConfigV1};
use snowq_generator::PydanticOptions;

pub fn get_pydantic_options(config: &Config) -> PydanticOptions {
    match config {
        Config::V1(ConfigV1 {
            pydantic: pydantic_options,
            ..
        }) => PydanticOptions {
            model_name_prefix: pydantic_options.model_name_prefix.clone(),
            model_name_suffix: pydantic_options.model_name_suffix.clone(),
        },
    }
}

pub fn get_schema_sync_output_dirpath(config: &Config) -> std::path::PathBuf {
    match config {
        Config::V1(ConfigV1 {
            model: snowq_config::ModelConfigV1 { output_dir, .. },
            ..
        }) => output_dir.clone(),
    }
}

pub fn get_snowflake_connection(
    config: &Config,
) -> Result<snowq_connector::Connection, anyhow::Error> {
    match config {
        Config::V1(ConfigV1 { connection, .. }) => snowq_connector::Connection::try_new(
            &connection.user.try_get_value()?,
            &connection.password.try_get_value()?,
            &connection.account.try_get_value()?,
            &connection.warehouse.try_get_value()?,
            &connection.database.try_get_value()?,
            &connection.schema.try_get_value()?,
        )
        .map_err(Into::into),
    }
}
