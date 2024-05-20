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
pub struct ConfigV1 {
    pub connection: Connection,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Connection {
    #[serde(default = "account_default")]
    pub account: StringOrEnv,

    #[serde(default = "username_default")]
    pub username: StringOrEnv,

    #[serde(default = "password_default")]
    pub password: StringOrEnv,
}

impl Default for Connection {
    fn default() -> Self {
        Connection {
            account: account_default(),
            username: username_default(),
            password: password_default(),
        }
    }
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

pub fn load() -> Result<Config, crate::Error> {
    let config_filename = "snowq.toml";

    // find recursively from current directory to root directory
    let mut current_dir = std::env::current_dir()?;
    loop {
        let config_path = current_dir.join(config_filename);
        if config_path.exists() {
            log::debug!("config file found: {:?}", config_path);

            let config = std::fs::read_to_string(config_path)?;
            return toml::from_str(&config).map_err(Into::into);
        }

        if !current_dir.pop() {
            break;
        }
    }

    Err(Error::ConfigFileNotFound)
}
