#[derive(Debug, clap::Args)]
pub struct Args {}

pub fn run(_args: Args) -> Result<(), anyhow::Error> {
    println!("{}", serde_json::to_string_pretty(&snowq_config::load()?)?);
    Ok(())
}
