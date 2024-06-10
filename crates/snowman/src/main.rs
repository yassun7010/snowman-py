mod app;
mod command;
mod config;
mod database;
mod formatter;

use console::Style;

fn main() {
    if let Err(err) = app::run(std::env::args_os()) {
        eprintln!(
            "{} {}",
            Style::new().on_red().white().bold().apply_to(" Error "),
            err
        );
        std::process::exit(1);
    }
}
