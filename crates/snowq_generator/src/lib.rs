mod pydantic;

pub use pydantic::{generate_pydantic_schema, generate_pydantic_table, PydanticOptions};

pub fn generate_modlue_init_py(database_names: &[&str]) -> String {
    database_names
        .iter()
        .map(|database_name| format!("from .import {database_name} as {database_name}"))
        .collect::<Vec<String>>()
        .join("\n")
        + "\n"
}
