use crate::traits::ToPythonModule;
use crate::ModelOptions;
use snowman_connector::schema::View;
use snowman_connector::Parameters;

use super::pydantic::generate_column;

pub fn generate_pydantic_views(
    views: &[View],
    model_options: &ModelOptions,
    params: &Parameters,
) -> String {
    views
        .iter()
        .map(|view| generate_pydantic_view(view, model_options, params))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_pydantic_view(
    view: &View,
    model_options: &ModelOptions,
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
        "class {}(snowman.View[\"_{}.{}\", \"_{}.{}\"]):\n",
        model_options
            .pydantic_options
            .make_class_name(&view.table_name),
        &view.schema_module(),
        model_options
            .column_accessor_options
            .make_class_name(&view.table_name),
        &view.schema_module(),
        model_options
            .order_item_accessor_options
            .make_class_name(&view.table_name)
    ));
    if let Some(comment) = &view.comment {
        if !comment.is_empty() {
            pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
        }
    }

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
