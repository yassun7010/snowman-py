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
        password: &str,
        account: &str,
        warehouse: &str,
        database: &str,
        schema: &str,
    ) -> Result<Self, snowflake_connector_rs::Error> {
        let client = SnowflakeClient::new(
            username,
            SnowflakeAuthMethod::Password(password.to_string()),
            SnowflakeClientConfig {
                account: account.to_string(),
                warehouse: Some(warehouse.to_string()),
                database: Some(database.to_string()),
                schema: Some(schema.to_string()),
                ..Default::default()
            },
        )?;
        Ok(Connection { inner: client })
    }

    pub async fn execute(
        &self,
        query: &str,
    ) -> Result<Vec<SnowflakeRow>, snowflake_connector_rs::Error> {
        let session = self.inner.create_session().await?;
        session.query(query).await
    }
}
