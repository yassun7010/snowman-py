use clap::{
    builder::styling::{AnsiColor, Color, Style},
    Parser,
};

use crate::command::{
    config::ConfigCommand,
    config_print::run_config_print_command,
    schema::{run_schema_sync_command, SchemaCommand},
    SubCommands,
};

#[derive(Debug, Parser)]
#[command(version, styles=app_styles())]
pub struct Args {
    #[command(subcommand)]
    pub subcommand: SubCommands,
}

impl<I, T> From<I> for Args
where
    I: IntoIterator<Item = T>,
    T: Into<std::ffi::OsString> + Clone,
{
    fn from(value: I) -> Self {
        Self::parse_from(value)
    }
}

pub fn run(args: impl Into<Args>) -> Result<(), Box<dyn std::error::Error>> {
    let args = args.into();

    dotenvy::dotenv()?;

    match args.subcommand {
        SubCommands::Schema(SchemaCommand::Sync(options)) => {
            tokio::runtime::Builder::new_multi_thread()
                .enable_all()
                .build()
                .unwrap()
                .block_on(async { run_schema_sync_command(options).await })?
        }
        SubCommands::Config(ConfigCommand::Print(command)) => run_config_print_command(command)?,
    }
    Ok(())
}

fn app_styles() -> clap::builder::Styles {
    clap::builder::Styles::styled()
        .usage(
            Style::new()
                .bold()
                .underline()
                .fg_color(Some(Color::Ansi(AnsiColor::BrightBlue))),
        )
        .header(
            Style::new()
                .bold()
                .underline()
                .fg_color(Some(Color::Ansi(AnsiColor::BrightBlue))),
        )
        .literal(Style::new().fg_color(Some(Color::Ansi(AnsiColor::Cyan))))
        .valid(
            Style::new()
                .bold()
                .underline()
                .fg_color(Some(Color::Ansi(AnsiColor::Green))),
        )
        .invalid(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Red))),
        )
        .error(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Red))),
        )
        .placeholder(Style::new().fg_color(Some(Color::Ansi(AnsiColor::BrightBlue))))
}
