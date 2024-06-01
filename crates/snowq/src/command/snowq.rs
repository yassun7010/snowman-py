use clap::Subcommand;
pub mod completion;

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Generate Python model classes from Snowflake dataabse schema.
    Completion(completion::Args),
}
