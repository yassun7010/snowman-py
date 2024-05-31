use clap::Subcommand;

use super::snowq_completion::SnowqCompletionCommand;

#[derive(Debug, Subcommand)]
pub enum SnowqCommand {
    /// Generate Python model classes from Snowflake dataabse schema.
    Completion(SnowqCompletionCommand),
}
