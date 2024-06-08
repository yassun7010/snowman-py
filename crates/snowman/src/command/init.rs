#[derive(clap::Args)]
pub struct Args {
    /// The file type of the Snowman configuration.
    #[arg(long, value_enum, default_value = "snowman.toml")]
    pub file: TargetFile,
}

#[derive(Copy, Clone, Default)]
pub enum TargetFile {
    /// Use "snowman.toml".
    #[default]
    SnowmanToml,

    /// Use "pyproject.toml".
    PyProjectToml,
}

impl clap::ValueEnum for TargetFile {
    fn value_variants<'a>() -> &'a [Self] {
        &[Self::SnowmanToml, Self::PyProjectToml]
    }

    fn to_possible_value<'a>(&self) -> Option<clap::builder::PossibleValue> {
        Some(match self {
            Self::SnowmanToml => clap::builder::PossibleValue::new("snowman.toml")
                .help("Create a new \"snowman.toml\" file."),
            Self::PyProjectToml => clap::builder::PossibleValue::new("pyproject.toml")
                .help("Append [tool.snowman] to the \"pyproject.toml\" file."),
        })
    }
}

impl From<TargetFile> for std::path::PathBuf {
    fn from(val: TargetFile) -> Self {
        match val {
            TargetFile::SnowmanToml => "snowman.toml".into(),
            TargetFile::PyProjectToml => "pyproject.toml".into(),
        }
    }
}

pub fn run(args: Args) -> Result<(), anyhow::Error> {
    let config_filepath: std::path::PathBuf = args.file.into();
    match args.file {
        TargetFile::SnowmanToml => {
            snowman_config::create_file(&config_filepath).map_err(Into::into)
        }
        TargetFile::PyProjectToml => {
            snowman_config::append_pyproject_tool(&config_filepath).map_err(Into::into)
        }
    }
}
