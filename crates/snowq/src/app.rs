use clap::{
    builder::styling::{AnsiColor, Color, Style},
    Parser,
};

use crate::command::{self, config, model, snowq};

#[derive(Debug, Parser)]
#[command(version, styles=app_styles())]
pub struct Args {
    #[command(subcommand)]
    pub subcommand: command::Command,
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
        command::Command::Model(model::Command::Generate(options)) => {
            tokio::runtime::Builder::new_multi_thread()
                .enable_all()
                .build()
                .unwrap()
                .block_on(async { crate::command::model::generate::run(options).await })?
        }
        command::Command::Config(command) => match command {
            config::Command::Create(args) => {
                config::create::run(args)?;
            }
            config::Command::Print(args) => {
                config::print::run(args)?;
            }
        },
        command::Command::Snowq(command) => match command {
            snowq::Command::Completion(command) => snowq::completion::run(command)?,
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
