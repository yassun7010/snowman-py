mod app;
mod command;
mod config;
use colored::Colorize;

fn main() {
    if let Err(err) = app::run(std::env::args_os()) {
        eprintln!("{} {}", " Error ".on_red().white().bold(), err);
        std::process::exit(1);
    }
}
