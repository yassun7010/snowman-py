// printout of the json schema for the snowman_config crate

use std::path::PathBuf;
use std::str::FromStr;

use snowman_config::Config;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let schema = schemars::schema_for!(Config);
    let schema = serde_json::to_string_pretty(&schema).unwrap();

    let output_dir =
        PathBuf::from_str(&std::env::args().nth(1).expect("need output_dirpath arg."))?;
    std::fs::write(output_dir.join("snowman.schema.json"), schema)?;

    Ok(())
}
