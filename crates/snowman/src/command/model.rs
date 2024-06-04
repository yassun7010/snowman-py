use clap::Subcommand;

pub mod generate;

#[derive(Subcommand)]
pub enum Command {
    /// Generate Python model classes from Snowflake dataabse schema.
    Generate(generate::Args),
}
