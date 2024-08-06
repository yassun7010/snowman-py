use clap::Subcommand;

pub mod diff;
pub mod generate;

#[derive(Subcommand)]
pub enum Command {
    /// Generate Python models from Snowflake database schemas.
    Generate(generate::Args),

    /// Generate differences between Python models and Snowflake database schemas.
    Diff(diff::Args),
}
