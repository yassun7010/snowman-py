use clap::{
    builder::styling::{AnsiColor, Color, Style},
    Parser,
};

use crate::command::{config, init, model, snowman, Command};

#[derive(Parser)]
#[command(version, styles=app_styles())]
pub struct Args {
    #[command(subcommand)]
    pub subcommand: Command,
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

pub fn run(args: impl Into<Args>) -> Result<(), anyhow::Error> {
    let args = args.into();

    dotenvy::dotenv()?;

    match args.subcommand {
        Command::Init(args) => init::run(args)?,
        Command::Model(command) => match command {
            model::Command::Generate(args) => tokio::runtime::Builder::new_multi_thread()
                .enable_all()
                .build()
                .unwrap()
                .block_on(async { model::generate::run(args).await })?,
            model::Command::Diff(args) => tokio::runtime::Builder::new_multi_thread()
                .enable_all()
                .build()
                .unwrap()
                .block_on(async { model::diff::run(args).await })?,
        },
        Command::Config(command) => match command {
            config::Command::Print(args) => {
                config::print::run(args)?;
            }
        },
        Command::Snowman(command) => match command {
            snowman::Command::Completion(command) => snowman::completion::run(command)?,
        },
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
