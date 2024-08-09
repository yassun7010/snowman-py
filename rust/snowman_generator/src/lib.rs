mod error;
pub mod formatter;
mod model;
mod sql;
mod traits;

pub use error::Error;
use itertools::Itertools;
pub use model::column_accessor::{
    generate_column_accessor, generate_column_accessors, get_column_accessor_modules,
    ColumnAccessorOptions,
};
pub use model::insert_typeddict::{
    generate_insert_typeddict, generate_insert_typeddicts, get_insert_typeddict_modules,
    InsertTypedDictOptions,
};
pub use model::pydantic::{get_pydantic_modules, PydanticOptions};
pub use model::pydantic_table::{generate_pydantic_table, generate_pydantic_tables};
pub use model::pydantic_view::{generate_pydantic_view, generate_pydantic_views};
pub use model::update_typeddict::{
    generate_update_typeddict, generate_update_typeddicts, get_update_typeddict_modules,
    UpdateTypedDictOptions,
};
use snowman_connector::query::DatabaseSchema;
use snowman_connector::schema::{Table, View};
pub use sql::generate_sql_definition;
pub use traits::{ToPython, ToPythonModule, ToSQL};

#[derive(Default)]
pub struct ModelOptions {
    pub column_accessor_options: ColumnAccessorOptions,
    pub insert_typeddict_options: InsertTypedDictOptions,
    pub update_typeddict_options: UpdateTypedDictOptions,
    pub pydantic_options: PydanticOptions,
}

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
    "if typing.TYPE_CHECKING:\n".to_string()
        + &inner_code
            .split('\n')
            .map(|line| {
                if line.is_empty() {
                    line.to_string()
                } else {
                    "    ".to_string() + line
                }
            })
            .join("\n")
}

pub async fn generate_schema_python_typehint(
    tables: &[Table],
    views: &[View],
    column_accessor_options: &ColumnAccessorOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
) -> Result<String, crate::Error> {
    let src = if tables.is_empty() && views.is_empty() {
        generate_module_docs().to_string()
    } else {
        itertools::join(
            [
                generate_module_docs(),
                &generate_import_modules(
                    &itertools::chain!(
                        get_column_accessor_modules(),
                        get_insert_typeddict_modules(),
                        get_update_typeddict_modules(),
                    )
                    .unique()
                    .sorted()
                    .collect::<Vec<&str>>(),
                ),
                &generate_column_accessors(tables, column_accessor_options),
                &generate_column_accessors(views, column_accessor_options),
                &generate_insert_typeddicts(tables, insert_typeddict_options),
                &generate_update_typeddicts(tables, update_typeddict_options),
            ],
            "\n",
        )
    };

    Ok(src)
}

pub async fn generate_schema_python_code(
    tables: &[Table],
    views: &[View],
    database_schema: &DatabaseSchema,
    model_options: &ModelOptions,
    params: &snowman_connector::Parameters,
) -> Result<String, crate::Error> {
    let schema_module_name = database_schema.schema_module();
    let src = if tables.is_empty() {
        generate_module_docs().to_string()
    } else {
        itertools::join(
            [
                generate_module_docs(),
                &generate_import_modules(
                    &itertools::chain!(
                        get_insert_typeddict_modules(),
                        get_update_typeddict_modules(),
                        get_pydantic_modules(),
                    )
                    .unique()
                    .sorted()
                    .collect::<Vec<&str>>(),
                ),
                &generate_type_checking(&format!(
                    "from . import _{schema_module_name} as _{schema_module_name}\n"
                )),
                &generate_pydantic_tables(
                    tables,
                    &model_options.pydantic_options,
                    &model_options.column_accessor_options,
                    &model_options.insert_typeddict_options,
                    &model_options.update_typeddict_options,
                    params,
                ),
                &generate_pydantic_views(
                    views,
                    &model_options.pydantic_options,
                    &model_options.column_accessor_options,
                    params,
                ),
            ],
            "\n",
        )
    };

    Ok(src)
}

pub async fn generate_database_init_python_code(
    schemas: &[&DatabaseSchema],
) -> Result<String, crate::Error> {
    let schema_names = schemas
        .iter()
        .map(|schema| schema.schema_module())
        .collect::<Vec<_>>();

    let src = itertools::join(
        [
            generate_module_docs(),
            &generate_modlue_init_py(
                &schema_names
                    .iter()
                    .map(AsRef::as_ref)
                    .collect::<Vec<&str>>(),
            ),
        ],
        "\n",
    );

    Ok(src)
}
