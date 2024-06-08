use clap::{CommandFactory, ValueEnum};
use clap_complete::{Generator, Shell};
use clap_complete_nushell::Nushell;

#[derive(clap::Args)]
pub struct Args {
    /// The shell to generate a completion script for (defaults to 'bash').
    #[arg(long)]
    shell: Option<ShellCompletion>,
}

#[derive(Debug, Clone, ValueEnum)]
enum ShellCompletion {
    /// Bourne Again SHell (bash)
    Bash,
    /// Elvish shell
    Elvish,
    /// Friendly Interactive SHell (fish)
    Fish,
    /// PowerShell
    PowerShell,
    /// Z SHell (zsh)
    Zsh,
    /// Nushell
    Nushell,
}

impl Generator for ShellCompletion {
    /// Generate the file name for the completion script.
    fn file_name(&self, name: &str) -> String {
        match self {
            ShellCompletion::Nushell => Nushell.file_name(name),
            ShellCompletion::Bash => Shell::Bash.file_name(name),
            ShellCompletion::Elvish => Shell::Elvish.file_name(name),
            ShellCompletion::Fish => Shell::Fish.file_name(name),
            ShellCompletion::PowerShell => Shell::PowerShell.file_name(name),
            ShellCompletion::Zsh => Shell::Zsh.file_name(name),
        }
    }

    /// Generate the completion script for the shell.
    fn generate(&self, cmd: &clap::Command, buf: &mut dyn std::io::Write) {
        match self {
            ShellCompletion::Nushell => Nushell.generate(cmd, buf),
            ShellCompletion::Bash => Shell::Bash.generate(cmd, buf),
            ShellCompletion::Elvish => Shell::Elvish.generate(cmd, buf),
            ShellCompletion::Fish => Shell::Fish.generate(cmd, buf),
            ShellCompletion::PowerShell => Shell::PowerShell.generate(cmd, buf),
            ShellCompletion::Zsh => Shell::Zsh.generate(cmd, buf),
        }
    }
}

pub fn run(args: Args) -> Result<(), anyhow::Error> {
    clap_complete::generate(
        args.shell.unwrap_or(ShellCompletion::Bash),
        &mut crate::app::Args::command(),
        "snowman",
        &mut std::io::stdout(),
    );
    Ok(())
}
