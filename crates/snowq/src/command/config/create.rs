#[derive(clap::Args)]
pub struct Args {
    #[clap(long)]
    pub overwrite: bool,
}

pub fn run(args: Args) -> Result<(), anyhow::Error> {
    let config_filepath = std::path::PathBuf::from("snowq.toml");
    if config_filepath.exists() && !args.overwrite {
        return Err(anyhow::anyhow!(format!(
            "{config_filepath:?} already exists."
        )));
    }

    snowq_config::create_file(&config_filepath)?;

    Ok(())
}
