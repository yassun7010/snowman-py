use crate::command::Args;

pub fn run(args: impl Into<Args>) -> Result<(), Box<dyn std::error::Error>> {
    let _ = args.into();
    Ok(())
}
