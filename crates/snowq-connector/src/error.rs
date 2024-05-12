#[derive(Debug, thiserror::Error)]

pub enum Error {
    #[error(transparent)]
    SnowflakeConnector(#[from] snowflake_connector_rs::Error),
    #[error("env var not found: {0}")]
    EnvVarNotFound(String),
}

impl Error {
    pub fn from_env_var(name: &str) -> Self {
        Self::EnvVarNotFound(name.to_string())
    }
}
