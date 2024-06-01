pub mod config;
pub mod config_create;
pub mod config_print;
pub mod model;
pub mod model_generate;
pub mod snowq;
pub mod snowq_completion;
use clap::Subcommand;

use self::{config::ConfigCommand, model::ModelCommand, snowq::SnowqCommand};

#[derive(Debug, Subcommand)]
pub enum SubCommands {
    /// Python model operations.
    #[command(subcommand)]
    Model(ModelCommand),

    /// snowq config operations.
    #[command(subcommand)]
    Config(ConfigCommand),

    /// snowq operations.
    #[command(subcommand)]
    #[command(name = "self")]
    Snowq(SnowqCommand),
}
