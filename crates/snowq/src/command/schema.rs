use clap::Subcommand;

pub use super::schema_sync::run_schema_sync_command;
use super::schema_sync::SchemaSyncCommand;

#[derive(Debug, Subcommand)]
pub enum SchemaCommand {
    /// Update Python schema classes from Snowflake dataabse schema.
    Sync(SchemaSyncCommand),
}
