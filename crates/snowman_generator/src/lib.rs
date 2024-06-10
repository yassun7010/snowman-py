mod model;

pub use model::pydantic::{
    generate_pydantic_model, generate_pydantic_models, get_pydantic_modules, PydanticOptions,
};

pub use model::update_typeddict::{
    generate_update_typeddict, generate_update_typeddicts, get_update_typeddict_modules,
    UpdateTypedDictOptions,
};

pub use model::insert_typeddict::{
    generate_insert_typeddict, generate_insert_typeddicts, get_insert_typeddict_modules,
    InsertTypedDictOptions,
};

pub fn generate_modlue_init_py(database_names: &[&str]) -> String {
    database_names
        .iter()
        .map(|database_name| format!("from .import {database_name} as {database_name}"))
        .collect::<Vec<String>>()
        .join("\n")
}

pub fn generate_import_modules(module_names: &[&str]) -> String {
    module_names
        .iter()
        .map(|module_name| format!("import {}", module_name))
        .collect::<Vec<String>>()
        .join("\n")
        + "\n"
}

pub fn generate_module_docs() -> &'static str {
    r#"#
# Code generated by snowman; DO NOT EDIT.
#
# For more information about snowman,
# please refer to https://github.com/yassun7010/snowman-py .
#
"#
}

pub fn generate_type_checking(inner_code: &str) -> String {
    ("if typing.TYPE_CHECKING:\n".to_string() + inner_code).replace('\n', "\n    ")
}
