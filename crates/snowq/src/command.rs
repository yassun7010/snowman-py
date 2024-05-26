pub mod config;
pub mod config_print;
pub mod new;
pub mod schema;
pub mod schema_generate;

use clap::Subcommand;

use self::{config::ConfigCommand, new::NewCommand, schema::SchemaCommand};

#[derive(Debug, Subcommand)]
pub enum SubCommands {
    /// Create a new snowq project.
    New(NewCommand),

    /// Snowflake schema operations.
    #[command(subcommand)]
    Schema(SchemaCommand),

    /// snowq config operations.
    #[command(subcommand)]
    Config(ConfigCommand),
}
