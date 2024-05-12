use snowflake_connector_rs::{
    SnowflakeAuthMethod, SnowflakeClient, SnowflakeClientConfig, SnowflakeRow,
};

mod error;
pub mod query;
pub mod schema;
pub use error::Error;

pub struct Connection {
    inner: SnowflakeClient,
}

impl Connection {
    pub fn try_new(
        username: &str,
        auth: SnowflakeAuthMethod,
        config: SnowflakeClientConfig,
    ) -> Result<Self, snowflake_connector_rs::Error> {
        let client = SnowflakeClient::new(username, auth, config)?;
        Ok(Connection { inner: client })
    }

    pub fn try_new_from_env() -> Result<Self, crate::Error> {
        Ok(Connection::try_new(
            &try_get_env("SNOWFLAKE_USER")?,
            SnowflakeAuthMethod::Password(try_get_env("SNOWFLAKE_PASSWORD")?),
            SnowflakeClientConfig {
                account: try_get_env("SNOWFLAKE_ACCOUNT")?,
                warehouse: try_get_env("SNOWFLAKE_WAREHOUSE").ok(),
                database: try_get_env("SNOWFLAKE_DATABASE").ok(),
                schema: try_get_env("SNOWFLAKE_SCHEMA").ok(),
                role: try_get_env("SNOWFLAKE_ROLE").ok(),
                timeout: None,
            },
        )?)
    }

    pub async fn execute(
        &self,
        query: &str,
    ) -> Result<Vec<SnowflakeRow>, snowflake_connector_rs::Error> {
        let session = self.inner.create_session().await?;
        Ok(session.query(query).await?)
    }
}

fn try_get_env(name: &str) -> Result<String, crate::Error> {
    std::env::var(name).map_err(|_| crate::Error::from_env_var(name))
}
