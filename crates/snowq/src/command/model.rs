use clap::Subcommand;

use super::model_generate;

#[derive(Debug, Subcommand)]
pub enum ModelCommand {
    /// Generate Python model classes from Snowflake dataabse schema.
    Generate(model_generate::Args),
}
