mod error;

use std::io::Write;

use serde::{Deserialize, Serialize};

pub use error::Error;

const CONFIG_FILENAME: &str = "snowman.toml";

#[doc(hidden)]
#[derive(Debug, Clone, Default, Serialize, Deserialize, schemars::JsonSchema)]
struct PyProjectToml {
    tool: Tool,
}

#[doc(hidden)]
#[derive(Debug, Clone, Default, Serialize, Deserialize, schemars::JsonSchema)]
struct Tool {
    snowman: Option<Config>,
}

#[doc(hidden)]
#[derive(Debug, Clone, Serialize, Deserialize, schemars::JsonSchema)]
pub enum ConfigSource {
    /// "snowman.toml" filepath.
    SnowmanToml(std::path::PathBuf),

    /// "pyproject.toml" filepath.
    PyProjectToml(std::path::PathBuf),
}

impl AsRef<std::path::Path> for ConfigSource {
    fn as_ref(&self) -> &std::path::Path {
        match self {
            ConfigSource::SnowmanToml(path) => path.as_ref(),
            ConfigSource::PyProjectToml(path) => path.as_ref(),
        }
    }
}

#[derive(Debug, Clone, Default, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Config {
    /// # The Snowflake connection configuration.
    pub connection: ConnectionV1,

    /// # The Python model configuration.
    ///
    /// It is mainly used for the Snowman model generate command.
    #[serde(default)]
    pub model: ModelConfigV1,

    /// # The Pydantic options.
    #[serde(default)]
    pub pydantic: PydanticOptionsV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct ConnectionV1 {
    /// # The Snowflake account name.
    #[serde(default = "account_default")]
    pub account: StringOrEnv,

    /// # The Snowflake user name.
    #[serde(default = "user_default")]
    pub user: StringOrEnv,

    /// # The Snowflake password.
    ///
    /// Currently only password authentication is supported.
    #[serde(default = "password_default")]
    pub password: StringOrEnv,

    /// # The Snowflake role.
    #[serde(default = "role_default")]
    pub role: StringOrEnv,

    /// # The Snowflake database.
    #[serde(default = "database_default")]
    pub database: StringOrEnv,

    /// # The Snowflake schema.
    #[serde(default = "schema_default")]
    pub schema: StringOrEnv,

    /// # The Snowflake warehouse.
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

#[derive(Debug, Clone, Serialize, Deserialize, Default, schemars::JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct ModelConfigV1 {
    /// # The output directory of the generated model.
    #[serde(default = "get_pwd")]
    pub output_dir: std::path::PathBuf,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default, schemars::JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct PydanticOptionsV1 {
    /// # The prefix of the model name.
    pub model_name_prefix: Option<String>,

    /// # The suffix of the model name.
    pub model_name_suffix: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
/// # Represents a string or an environment variable.
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

#[derive(Debug, Clone, Serialize, Deserialize, schemars::JsonSchema)]
pub struct Env {
    /// # The environment variable name.
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

pub fn find_path() -> Result<ConfigSource, crate::Error> {
    // find recursively from current directory to root directory
    let mut current_dir = std::env::current_dir().unwrap();
    loop {
        let config_path = current_dir.join(CONFIG_FILENAME);
        if config_path.exists() {
            log::debug!("\"snowq.toml\" found: {:?}", config_path);

            return Ok(ConfigSource::SnowmanToml(config_path));
        }

        let pyproject_toml_path = current_dir.join("pyproject.toml");
        if pyproject_toml_path.exists() {
            log::debug!("\"pyproject.toml\" found: {:?}", pyproject_toml_path);

            return Ok(ConfigSource::PyProjectToml(pyproject_toml_path));
        }

        if !current_dir.pop() {
            break;
        }
    }

    Err(Error::ConfigFileNotFound(CONFIG_FILENAME.into()))
}

pub fn load_from_source(source: &ConfigSource) -> Result<Config, crate::Error> {
    match source {
        ConfigSource::PyProjectToml(path) => {
            let pyproject_toml = std::fs::read_to_string(path)?;
            let pyproject_toml: PyProjectToml = toml::from_str(&pyproject_toml)?;

            if let Some(config) = pyproject_toml.tool.snowman {
                Ok(config)
            } else {
                Err(Error::ConfigFileNotFound(CONFIG_FILENAME.into()))
            }
        }
        ConfigSource::SnowmanToml(path) => {
            let config = std::fs::read_to_string(path)?;
            toml::from_str(&config).map_err(Into::into)
        }
    }
}

pub fn load() -> Result<Config, crate::Error> {
    load_from_source(&find_path()?)
}

fn get_pwd() -> std::path::PathBuf {
    ".".into()
}

pub fn write_as_toml(config: &Config, filepath: &std::path::Path) -> Result<(), crate::Error> {
    let file = std::fs::File::create(filepath)?;
    let mut writer = std::io::BufWriter::new(file);
    let toml = toml::to_string(&config)?;
    writer.write_all(toml.as_bytes())?;

    Ok(())
}

pub fn create_file(filepath: &std::path::Path) -> Result<(), crate::Error> {
    std::fs::File::create(filepath)?
        .write_all(DEFAULT_CONFIG_STRING.as_bytes())
        .map_err(Into::into)
}

const DEFAULT_CONFIG_STRING: &str = r#"# [Snowman](https://github.com/yassun7010/snowman)
#:schema https://raw.githubusercontent.com/yassun7010/snowman-py/main/docs/snowman.schema.json

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
