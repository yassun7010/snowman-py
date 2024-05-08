use clap::Args;

#[derive(Debug, Args)]
pub struct SchemaSync {}

pub fn run_schema_sync_command(_: SchemaSync) -> Result<(), Box<dyn std::error::Error>> {
    Ok(())
}
