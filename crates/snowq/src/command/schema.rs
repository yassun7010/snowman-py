use clap::Subcommand;

pub use super::schema_generate::run_schema_generate_command;
use super::schema_generate::SchemaGenerateCommand;

#[derive(Debug, Subcommand)]
pub enum SchemaCommand {
    /// Generate Python schema classes from Snowflake dataabse schema.
    Generate(SchemaGenerateCommand),
}
