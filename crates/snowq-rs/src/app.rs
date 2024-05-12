use crate::command::{
    schema::{run_schema_sync_command, Schema},
    Args, SubCommands,
};

pub fn run(args: impl Into<Args>) -> Result<(), Box<dyn std::error::Error>> {
    let args = args.into();

    dotenvy::dotenv()?;

    match args.subcommand {
        SubCommands::Schema(Schema::Sync(options)) => tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .build()
            .unwrap()
            .block_on(async { run_schema_sync_command(options).await })?,
    }
    Ok(())
}
