use clap::Subcommand;

pub mod print;

#[derive(Subcommand)]
pub enum Command {
    /// Create a new configuration file.
    Create(super::init::Args),

    /// Print the current configuration.
    Print(print::Args),
}
