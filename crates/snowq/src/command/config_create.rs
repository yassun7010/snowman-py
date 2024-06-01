#[derive(Debug, clap::Args)]
pub struct Args {}

pub fn run(_args: Args) -> Result<(), anyhow::Error> {
    let config_filepath = std::path::PathBuf::from("snowq.toml");
    if config_filepath.exists() {
        return Err(anyhow::anyhow!(format!(
            "{config_filepath:?} already exists."
        )));
    }

    snowq_config::write_new_file(&config_filepath)?;

    Ok(())
}
