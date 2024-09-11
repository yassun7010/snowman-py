use crate::model::pydantic::PydanticOptions;
use crate::traits::ToPythonModule;
use crate::{ColumnAccessorOptions, InsertTypedDictOptions, UpdateTypedDictOptions};
use snowman_connector::schema::Table;
use snowman_connector::Parameters;

use super::pydantic::generate_column;

pub fn generate_pydantic_tables(
    tables: &[Table],
    pydantic_options: &PydanticOptions,
    column_accessor_options: &ColumnAccessorOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
    params: &Parameters,
) -> String {
    tables
        .iter()
        .map(|table| {
            generate_pydantic_table(
                table,
                pydantic_options,
                column_accessor_options,
                insert_typeddict_options,
                update_typeddict_options,
                params,
            )
        })
        .collect::<Vec<String>>()
        .join("\n\n")
}

pub fn generate_pydantic_table(
    table: &Table,
    pydantic_options: &PydanticOptions,
    column_accessor_options: &ColumnAccessorOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
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
    let table_class_name = pydantic_options.make_class_name(&table.table_name);
    let schema_module_name = table.schema_module();
    pydantic_schema.push_str(&format!(
        "class {}(snowman.Table[\"{}\", \"_{}.{}\", \"_{}.{}\", \"_{}.{}\"]):\n",
        table_class_name,
        table_class_name,
        schema_module_name,
        column_accessor_options.make_class_name(&table.table_name),
        schema_module_name,
        insert_typeddict_options.make_class_name(&table.table_name),
        schema_module_name,
        update_typeddict_options.make_class_name(&table.table_name)
    ));
    if let Some(comment) = &table.comment {
        if !comment.is_empty() {
            pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
        }
    }

    pydantic_schema.push_str("    model_config = pydantic.ConfigDict(populate_by_name=True)\n");

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
