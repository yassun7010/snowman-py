#[derive(clap::Args)]
pub struct Args {
    /// The file type of the Snowman configuration.
    #[arg(long, value_enum, default_value = "snowman.toml")]
    pub file: TargetFile,
}

#[derive(Clone, Default)]
pub enum TargetFile {
    #[default]
    SnowmanToml,
    // PyProjectToml,
}

impl clap::ValueEnum for TargetFile {
    fn value_variants<'a>() -> &'a [Self] {
        &[TargetFile::SnowmanToml]
    }

    fn to_possible_value<'a>(&self) -> Option<clap::builder::PossibleValue> {
        Some(match self {
            TargetFile::SnowmanToml => clap::builder::PossibleValue::new("snowman.toml"),
        })
    }
}

impl From<TargetFile> for std::path::PathBuf {
    fn from(val: TargetFile) -> Self {
        match val {
            TargetFile::SnowmanToml => "snowman.toml".into(),
        }
    }
}

pub fn run(args: Args) -> Result<(), anyhow::Error> {
    match args.file {
        TargetFile::SnowmanToml => {
            let config_filepath: std::path::PathBuf = args.file.into();
            if config_filepath.exists() {
                return Err(anyhow::anyhow!(format!(
                    "{config_filepath:?} already exists."
                )));
            }
            snowman_config::create_file(&config_filepath)?;
        }
    };

    Ok(())
}
