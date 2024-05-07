use clap::Subcommand;

use super::schema_sync::SchemaSync;

#[derive(Debug, Subcommand)]
pub enum Schema {
    /// Update Python schema classes from Snowflake dataabse schema.
    Sync(SchemaSync),
}
