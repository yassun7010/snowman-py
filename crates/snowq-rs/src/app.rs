use crate::command::{
    schema::{run_schema_sync_command, Schema},
    Args, SubCommands,
};

pub fn run(args: impl Into<Args>) -> Result<(), Box<dyn std::error::Error>> {
    let args = args.into();
    match args.subcommand {
        SubCommands::Schema(Schema::Sync(options)) => run_schema_sync_command(options)?,
    }
    Ok(())
}
