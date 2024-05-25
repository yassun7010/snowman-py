pub mod config;
pub mod config_print;
pub mod schema;
pub mod schema_sync;

use clap::Subcommand;

use self::{config::ConfigCommand, schema::SchemaCommand};

#[derive(Debug, Subcommand)]
pub enum SubCommands {
    /// Snowflake schema operations.
    #[command(subcommand)]
    Schema(SchemaCommand),

    /// snowq config operations.
    #[command(subcommand)]
    Config(ConfigCommand),
}
