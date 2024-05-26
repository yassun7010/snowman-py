use clap::Args;

#[derive(Debug, Args)]
pub struct ConfigPrintCommand {}

pub fn run_config_print_command(_command: ConfigPrintCommand) -> Result<(), anyhow::Error> {
    println!("{}", serde_json::to_string_pretty(&snowq_config::load()?)?);
    Ok(())
}
