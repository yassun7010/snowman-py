// printout of the json schema for the snowman_config crate

use snowman_config::Config;

fn main() {
    let schema = schemars::schema_for!(Config);
    let schema = serde_json::to_string_pretty(&schema).unwrap();
    println!("{}", schema);
}
