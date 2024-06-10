#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    SnowmanConnector(#[from] snowman_connector::Error),
}
