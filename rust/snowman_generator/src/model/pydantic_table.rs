use crate::traits::ToPythonModule;
use crate::ModelOptions;
use snowman_connector::schema::Table;
use snowman_connector::Parameters;

use super::pydantic::generate_column;

pub fn generate_pydantic_tables(
    tables: &[Table],
    model_options: &ModelOptions,
    params: &Parameters,
) -> String {
    tables
        .iter()
        .map(|table| generate_pydantic_table(table, model_options, params))
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_pydantic_table(
    table: &Table,
    model_options: &ModelOptions,
    params: &Parameters,
) -> String {
    let mut pydantic_schema = String::new();

    pydantic_schema.push_str(&format!(
        "# TABLE: {}.{}.{}\n",
        table.database_name, table.schema_name, table.table_name,
    ));
    pydantic_schema.push_str(&format!(
        "@snowman.table(\"{}\", \"{}\", \"{}\")\n",
        table.database_name, table.schema_name, table.table_name,
    ));
    let table_class_name = model_options
        .pydantic_options
        .make_class_name(&table.table_name);
    let schema_module_name = table.schema_module();
    let column_accessor_class_name = model_options
        .column_accessor_options
        .make_class_name(&table.table_name);
    let order_item_accessor_class_name = model_options
        .order_item_accessor_options
        .make_class_name(&table.table_name);
    let insert_typeddict_class_name = model_options
        .insert_typeddict_options
        .make_class_name(&table.table_name);
    let update_typeddict_class_name = model_options
        .update_typeddict_options
        .make_class_name(&table.table_name);

    pydantic_schema.push_str(&format!(
        "class {table_class_name}(snowman.Table[\"{table_class_name}\", \"_{schema_module_name}.{column_accessor_class_name}\", \"_{schema_module_name}.{order_item_accessor_class_name}\", \"_{schema_module_name}.{insert_typeddict_class_name}\", \"_{schema_module_name}.{update_typeddict_class_name}\"]):\n",
    ));
    if let Some(comment) = &table.comment {
        if !comment.is_empty() {
            pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
        }
    }

    for column in &table.columns {
        pydantic_schema.push_str(&format!("\n    {}", generate_column(column, params)));

        if let Some(comment) = column.comment.as_ref() {
            if !comment.is_empty() {
                pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
            }
        }
    }
    pydantic_schema
}
