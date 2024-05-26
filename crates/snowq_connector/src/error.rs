#[derive(Debug, thiserror::Error)]

pub enum Error {
    #[error(transparent)]
    SnowflakeConnector(#[from] snowflake_connector_rs::Error),
}
