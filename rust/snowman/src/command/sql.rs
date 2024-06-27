use clap::Subcommand;

pub mod generate;

#[derive(Subcommand)]
pub enum Command {
    /// Generate Python models from Snowflake database schemas.
    Generate(generate::Args),
}
