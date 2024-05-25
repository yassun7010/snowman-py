mod pydantic;

pub use pydantic::{
    generate_pydantic_model, generate_pydantic_models, get_pydantic_modules, PydanticOptions,
};

pub fn generate_modlue_init_py(database_names: &[&str]) -> String {
    database_names
        .iter()
        .map(|database_name| format!("from .import {database_name} as {database_name}"))
        .collect::<Vec<String>>()
        .join("\n")
        + "\n"
}

pub fn generate_import_modules(module_names: &[&str]) -> String {
    module_names
        .iter()
        .map(|module_name| format!("import {}", module_name))
        .collect::<Vec<String>>()
        .join("\n")
        + "\n\n\n"
}