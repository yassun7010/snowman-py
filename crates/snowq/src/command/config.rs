use clap::Subcommand;
pub mod create;
pub mod print;

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Create a new configuration file.
    Create(create::Args),

    /// Print the current configuration.
    Print(print::Args),
}
