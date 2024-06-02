// printout of the json schema for the snowq_config crate

use snowq_config::Config;

fn main() {
    let schema = schemars::schema_for!(Config);
    let schema = serde_json::to_string_pretty(&schema).unwrap();
    println!("{}", schema);
}
