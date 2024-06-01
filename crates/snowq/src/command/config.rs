use clap::Subcommand;

use super::{config_create, config_print};

#[derive(Debug, Subcommand)]
pub enum ConfigCommand {
    /// Create a new configuration file.
    Create(config_create::Args),

    /// Print the current configuration.
    Print(config_print::Args),
}
