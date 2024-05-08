use clap::Subcommand;

pub use super::schema_sync::{run_schema_sync_command, SchemaSync};

#[derive(Debug, Subcommand)]
pub enum Schema {
    /// Update Python schema classes from Snowflake dataabse schema.
    Sync(SchemaSync),
}
