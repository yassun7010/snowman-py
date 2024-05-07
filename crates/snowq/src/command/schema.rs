use clap::Subcommand;

use super::schema_sync::SchemaSync;

#[derive(Debug, Subcommand)]
pub enum Schema {
    Sync(SchemaSync),
}
