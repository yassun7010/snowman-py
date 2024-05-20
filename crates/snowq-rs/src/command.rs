pub mod config;
pub mod config_print;
pub mod schema;
pub mod schema_sync;

use clap::{Parser, Subcommand};

use self::{config::ConfigCommand, schema::SchemaCommand};

#[derive(Debug, Parser)]
pub struct Args {
    #[command(subcommand)]
    pub subcommand: SubCommands,
}

#[derive(Debug, Subcommand)]
pub enum SubCommands {
    /// Snowflake schema operations.
    #[command(subcommand)]
    Schema(SchemaCommand),

    /// snowq config operations.
    #[command(subcommand)]
    Config(ConfigCommand),
}

impl<I, T> From<I> for Args
where
    I: IntoIterator<Item = T>,
    T: Into<std::ffi::OsString> + Clone,
{
    fn from(value: I) -> Self {
        Self::parse_from(value)
    }
}
