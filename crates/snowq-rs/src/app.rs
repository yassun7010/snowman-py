use crate::command::{
    config::ConfigCommand,
    config_print::run_config_print_command,
    schema::{run_schema_sync_command, SchemaCommand},
    Args, SubCommands,
};

pub fn run(args: impl Into<Args>) -> Result<(), Box<dyn std::error::Error>> {
    let args = args.into();

    dotenvy::dotenv()?;

    match args.subcommand {
        SubCommands::Schema(SchemaCommand::Sync(options)) => {
            tokio::runtime::Builder::new_multi_thread()
                .enable_all()
                .build()
                .unwrap()
                .block_on(async { run_schema_sync_command(options).await })?
        }
        SubCommands::Config(ConfigCommand::Print(command)) => run_config_print_command(command)?,
    }
    Ok(())
}
