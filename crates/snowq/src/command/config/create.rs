#[derive(clap::Args)]
pub struct Args {
    /// The path to the snowq configuration file.
    #[arg(long, default_value = "snowq.toml")]
    pub file: std::path::PathBuf,

    /// Overwrite the existing configuration file.
    #[arg(long)]
    pub overwrite: bool,
}

pub fn run(args: Args) -> Result<(), anyhow::Error> {
    let config_filepath = args.file;
    if config_filepath.exists() && !args.overwrite {
        return Err(anyhow::anyhow!(format!(
            "{config_filepath:?} already exists."
        )));
    }

    snowq_config::create_file(&config_filepath)?;

    Ok(())
}
