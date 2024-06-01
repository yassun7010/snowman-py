pub mod config;
pub mod model;
pub mod snowq;
use clap::Subcommand;

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Python model operations.
    #[command(subcommand)]
    Model(model::Command),

    /// Snowq config operations.
    #[command(subcommand)]
    Config(config::Command),

    /// Snowq operations.
    #[command(subcommand)]
    #[command(name = "self")]
    Snowq(snowq::Command),
}
