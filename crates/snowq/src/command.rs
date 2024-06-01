pub mod config;
pub mod model;
pub mod snowq;
use clap::Subcommand;

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Python model operations.
    #[command(subcommand)]
    Model(model::Command),

    /// snowq config operations.
    #[command(subcommand)]
    Config(config::Command),

    /// snowq operations.
    #[command(subcommand)]
    #[command(name = "self")]
    Snowq(snowq::Command),
}
