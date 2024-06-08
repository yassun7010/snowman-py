use clap::Subcommand;

pub mod print;

#[derive(Subcommand)]
pub enum Command {
    /// Print the current configuration.
    Print(print::Args),
}
