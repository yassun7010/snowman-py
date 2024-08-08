use crate::model::pydantic::PydanticOptions;
use crate::traits::ToPythonModule;
use crate::ColumnAccessorOptions;
use snowman_connector::schema::View;
use snowman_connector::Parameters;

use super::pydantic::generate_column;

pub fn generate_pydantic_views(
    views: &[View],
    pydantic_options: &PydanticOptions,
    column_accessor_options: &ColumnAccessorOptions,
    params: &Parameters,
) -> String {
    views
        .iter()
        .map(|view| generate_pydantic_view(view, pydantic_options, column_accessor_options, params))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_pydantic_view(
    view: &View,
    pydantic_options: &PydanticOptions,
    column_accessor_options: &ColumnAccessorOptions,
    params: &Parameters,
) -> String {
    let mut pydantic_schema = String::new();

    pydantic_schema.push_str(&format!(
        "# VIEW: {}.{}.{}\n",
        view.database_name, view.schema_name, view.table_name,
    ));
    pydantic_schema.push_str(&format!(
        "@snowman.view(\"{}\", \"{}\", \"{}\")\n",
        view.database_name, view.schema_name, view.table_name,
    ));
    pydantic_schema.push_str(&format!(
        "class {}(snowman.View[\"_{}.{}\"]):\n",
        pydantic_options.make_class_name(&view.table_name),
        view.schema_module(),
        column_accessor_options.make_class_name(&view.table_name)
    ));
    if let Some(comment) = &view.comment {
        if !comment.is_empty() {
            pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
        }
    }

    pydantic_schema.push_str("    model_config = pydantic.ConfigDict(populate_by_name=True)\n");

    for column in &view.columns {
        pydantic_schema.push_str(&format!("\n    {}", generate_column(column, params)));

        if let Some(comment) = column.comment.as_ref() {
            if !comment.is_empty() {
                pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
            }
        }
    }
    pydantic_schema
}
