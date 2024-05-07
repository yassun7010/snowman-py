mod schema;
mod schema_sync;

use clap::{Parser, Subcommand};

use self::schema::Schema;

#[derive(Debug, Parser)]
pub struct Args {
    #[command(subcommand)]
    subcommand: SubCommands,
}

#[derive(Debug, Subcommand)]
enum SubCommands {
    /// Snowflake schema operations.
    #[command(subcommand)]
    Schema(Schema),
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
