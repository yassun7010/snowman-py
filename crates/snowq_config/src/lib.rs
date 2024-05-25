mod error;
use serde::{Deserialize, Serialize};

pub use error::Error;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "version")]
pub enum Config {
    #[serde(rename = "v1")]
    V1(ConfigV1),
}

impl Default for Config {
    fn default() -> Self {
        Config::V1(ConfigV1::default())
    }
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConfigV1 {
    pub connection: ConnectionV1,

    #[serde(default)]
    pub schema: SchemaConfigV1,

    #[serde(default)]
    pub pydantic: PydanticOptionsV1,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConnectionV1 {
    #[serde(default = "account_default")]
    pub account: StringOrEnv,

    #[serde(default = "username_default")]
    pub username: StringOrEnv,

    #[serde(default = "password_default")]
    pub password: StringOrEnv,
}

impl Default for ConnectionV1 {
    fn default() -> Self {
        ConnectionV1 {
            account: account_default(),
            username: username_default(),
            password: password_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct SchemaConfigV1 {
    #[serde(default = "get_pwd")]
    pub output_dir: std::path::PathBuf,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct PydanticOptionsV1 {
    pub model_name_prefix: Option<String>,
    pub model_name_suffix: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum StringOrEnv {
    String(String),
    Env(Env),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Env {
    env: String,
}

fn account_default() -> StringOrEnv {
    StringOrEnv::Env(Env {
        env: "SNOWFLAKE_ACCOUNT".to_string(),
    })
}

fn username_default() -> StringOrEnv {
    StringOrEnv::Env(Env {
        env: "SNOWFLAKE_USER".to_string(),
    })
}

fn password_default() -> StringOrEnv {
    StringOrEnv::Env(Env {
        env: "SNOWFLAKE_PASSWORD".to_string(),
    })
}

pub fn find_path() -> Result<std::path::PathBuf, crate::Error> {
    let config_filename = "snowq.toml";

    // find recursively from current directory to root directory
    let mut current_dir = std::env::current_dir()?;
    loop {
        let config_path = current_dir.join(config_filename);
        if config_path.exists() {
            log::debug!("config file found: {:?}", config_path);

            return Ok(config_path);
        }

        if !current_dir.pop() {
            break;
        }
    }

    Err(Error::ConfigFileNotFound)
}

pub fn load_from_path(path: &std::path::Path) -> Result<Config, crate::Error> {
    let config = std::fs::read_to_string(path)?;
    toml::from_str(&config).map_err(Into::into)
}

pub fn load() -> Result<Config, crate::Error> {
    let config_path = find_path()?;
    load_from_path(&config_path)
}

fn get_pwd() -> std::path::PathBuf {
    std::env::current_dir().unwrap_or_default()
}
