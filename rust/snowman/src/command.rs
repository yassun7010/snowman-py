pub mod config;
pub mod init;
pub mod model;
pub mod snowman;
pub mod sql;
use clap::Subcommand;

#[derive(Subcommand)]
pub enum Command {
    /// Create a new configuration file.
    Init(init::Args),

    /// Python model operations.
    #[command(subcommand)]
    Model(model::Command),

    /// SQL operations.
    #[command(subcommand)]
    Sql(sql::Command),

    /// Snowman config operations.
    #[command(subcommand)]
    Config(config::Command),

    /// Snowman operations.
    #[command(subcommand)]
    #[command(name = "self")]
    Snowman(snowman::Command),
}
