use snowman_config::Config;
use snowman_generator::PydanticOptions;

pub fn get_pydantic_options(config: &Config) -> PydanticOptions {
    let Config {
        pydantic: pydantic_options,
        ..
    } = config;

    PydanticOptions {
        model_name_prefix: pydantic_options.model_name_prefix.clone(),
        model_name_suffix: pydantic_options.model_name_suffix.clone(),
    }
}

pub fn get_model_output_dirpath(config: &Config) -> std::path::PathBuf {
    let Config {
        model: snowman_config::ModelConfigV1 { output_dir, .. },
        ..
    } = config;

    output_dir.clone()
}

pub fn get_snowflake_connection(
    config: &Config,
) -> Result<snowman_connector::Connection, anyhow::Error> {
    let Config { connection, .. } = config;

    snowman_connector::Connection::try_new(
        connection.user.try_get_value()?,
        connection.password.try_get_value()?,
        connection.account.try_get_value()?,
        connection.warehouse.try_get_value()?,
        connection.role.try_get_value()?,
        connection.database.try_get_value()?,
        connection
            .schema
            .as_ref()
            .and_then(|v| v.try_get_value().ok()),
    )
    .map_err(Into::into)
}
