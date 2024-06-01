mod error;

use std::io::Write;

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
    pub model: ModelConfigV1,

    #[serde(default)]
    pub pydantic: PydanticOptionsV1,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ConnectionV1 {
    #[serde(default = "account_default")]
    pub account: StringOrEnv,

    #[serde(default = "user_default")]
    pub user: StringOrEnv,

    #[serde(default = "password_default")]
    pub password: StringOrEnv,

    #[serde(default = "role_default")]
    pub role: StringOrEnv,

    #[serde(default = "database_default")]
    pub database: StringOrEnv,

    #[serde(default = "schema_default")]
    pub schema: StringOrEnv,

    #[serde(default = "warehouse_default")]
    pub warehouse: StringOrEnv,
}

impl Default for ConnectionV1 {
    fn default() -> Self {
        ConnectionV1 {
            account: account_default(),
            user: user_default(),
            password: password_default(),
            role: role_default(),
            database: database_default(),
            schema: schema_default(),
            warehouse: warehouse_default(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct ModelConfigV1 {
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

impl StringOrEnv {
    pub fn try_get_value(&self) -> Result<String, crate::Error> {
        match self {
            StringOrEnv::String(s) => Ok(s.clone()),
            StringOrEnv::Env(env) => {
                std::env::var(&env.env).map_err(|_| crate::Error::from_env_var(&env.env))
            }
        }
    }
}

pub fn new_env(env: &str) -> StringOrEnv {
    StringOrEnv::Env(Env {
        env: env.to_string(),
    })
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Env {
    env: String,
}

fn account_default() -> StringOrEnv {
    new_env("SNOWFLAKE_ACCOUNT")
}

fn user_default() -> StringOrEnv {
    new_env("SNOWFLAKE_USER")
}

fn password_default() -> StringOrEnv {
    new_env("SNOWFLAKE_PASSWORD")
}

fn role_default() -> StringOrEnv {
    new_env("SNOWFLAKE_ROLE")
}

fn database_default() -> StringOrEnv {
    new_env("SNOWFLAKE_DATABASE")
}

fn schema_default() -> StringOrEnv {
    new_env("SNOWFLAKE_SCHEMA")
}

fn warehouse_default() -> StringOrEnv {
    new_env("SNOWFLAKE_WAREHOUSE")
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

    Err(Error::ConfigFileNotFound("snowq.toml".into()))
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

pub fn write_as_toml(config: &Config, filepath: &std::path::Path) -> Result<(), crate::Error> {
    let file = std::fs::File::create(filepath)?;
    let mut writer = std::io::BufWriter::new(file);
    let toml = toml::to_string(&config)?;
    writer.write_all(toml.as_bytes())?;

    Ok(())
}

pub fn write_new_file(filepath: &std::path::Path) -> Result<(), crate::Error> {
    std::fs::File::create(filepath)?
        .write_all(DEFAULT_CONFIG_STRING.as_bytes())
        .map_err(Into::into)
}

const DEFAULT_CONFIG_STRING: &str = r#"# snowq
version = "v1"

[connection]
account = { env = "SNOWFLAKE_ACCOUNT" }
user = { env = "SNOWFLAKE_USER" }
password = { env = "SNOWFLAKE_PASSWORD" }
role = { env = "SNOWFLAKE_ROLE" }
database = { env = "SNOWFLAKE_DATABASE" }
schema = { env = "SNOWFLAKE_SCHEMA" }
warehouse = { env = "SNOWFLAKE_WAREHOUSE" }

[model]
output_dir = "."

[pydantic]
# model_name_suffix = "Model"
"#;

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_parse_default_config_string() {
        toml::from_str::<Config>(super::DEFAULT_CONFIG_STRING).unwrap();
    }
}
