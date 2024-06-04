pub mod config;
pub mod model;
pub mod snowman;
use clap::Subcommand;

#[derive(Subcommand)]
pub enum Command {
    /// Python model operations.
    #[command(subcommand)]
    Model(model::Command),

    /// Snowman config operations.
    #[command(subcommand)]
    Config(config::Command),

    /// Snowman operations.
    #[command(subcommand)]
    #[command(name = "self")]
    Snowman(snowman::Command),
}
