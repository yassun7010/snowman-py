mod app;
mod command;
mod config;

fn main() {
    if let Err(err) = app::run(std::env::args_os()) {
        eprintln!("Error: {}", err);
        std::process::exit(1);
    }
}
