#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    IO(#[from] std::io::Error),

    #[error(transparent)]
    TomlSerialize(#[from] toml::ser::Error),

    #[error(transparent)]
    TomlDeserialize(#[from] toml::de::Error),

    #[error("Config file not found")]
    ConfigFileNotFound,

    #[error("env var not found: {0}")]
    EnvVarNotFound(String),
}

impl Error {
    pub fn from_env_var(name: &str) -> Self {
        Self::EnvVarNotFound(name.to_string())
    }
}
