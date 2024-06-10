use clap::Subcommand;

pub mod diff;
pub mod generate;

#[derive(Subcommand)]
pub enum Command {
    /// Generate Python model classes from Snowflake dataabse schema.
    Generate(generate::Args),

    /// Generate diff between Python model classes and Snowflake dataabse schema.
    Diff(diff::Args),
}
