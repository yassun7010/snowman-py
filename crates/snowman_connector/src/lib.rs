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
        username: String,
        password: String,
        account: String,
        warehouse: String,
        role: String,
        database: String,
        schema: Option<String>,
    ) -> Result<Self, snowflake_connector_rs::Error> {
        log::debug!("username: {username}");
        log::debug!(
            "password: {}**********{}",
            &password[..2],
            &password[password.len() - 2..]
        );
        log::debug!("account: {account}");
        log::debug!("warehouse: {warehouse}");
        log::debug!("role: {role}");
        log::debug!("database: {database}");
        log::debug!("schema: {schema:?}");

        let client = SnowflakeClient::new(
            &username,
            SnowflakeAuthMethod::Password(password),
            SnowflakeClientConfig {
                account,
                warehouse: Some(warehouse),
                role: Some(role),
                database: Some(database),
                schema: schema.map(|s| s.to_string()),
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
