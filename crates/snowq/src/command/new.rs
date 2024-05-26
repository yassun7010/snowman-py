use clap::Args;

#[derive(Debug, Args)]
pub struct NewCommand {}

pub fn run_new_command(_command: NewCommand) -> Result<(), anyhow::Error> {
    let config_filepath = std::path::PathBuf::from("snowq.toml");
    if config_filepath.exists() {
        return Err(anyhow::anyhow!(format!(
            "{config_filepath:?} already exists."
        )));
    }

    snowq_config::write_new_file(&config_filepath)?;

    Ok(())
}
