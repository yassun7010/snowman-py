pub mod config;
pub mod config_print;
pub mod model;
pub mod model_generate;
pub mod new;

use clap::Subcommand;

use self::{config::ConfigCommand, model::ModelCommand, new::NewCommand};

#[derive(Debug, Subcommand)]
pub enum SubCommands {
    /// Create a new snowq project.
    New(NewCommand),

    /// Python model operations.
    #[command(subcommand)]
    Model(ModelCommand),

    /// snowq config operations.
    #[command(subcommand)]
    Config(ConfigCommand),
}
