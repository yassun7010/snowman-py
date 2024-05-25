use clap::Subcommand;

use super::config_print::ConfigPrintCommand;

#[derive(Debug, Subcommand)]
pub enum ConfigCommand {
    /// Print the current configuration.
    Print(ConfigPrintCommand),
}
