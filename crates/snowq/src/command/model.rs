use clap::Subcommand;

pub use super::model_generate::run_model_generate_command;
use super::model_generate::ModelGenerateCommand;

#[derive(Debug, Subcommand)]
pub enum ModelCommand {
    /// Generate Python model classes from Snowflake dataabse schema.
    Generate(ModelGenerateCommand),
}
