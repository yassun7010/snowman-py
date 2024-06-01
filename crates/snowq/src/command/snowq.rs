use clap::Subcommand;

use super::snowq_completion;

#[derive(Debug, Subcommand)]
pub enum SnowqCommand {
    /// Generate Python model classes from Snowflake dataabse schema.
    Completion(snowq_completion::Args),
}
