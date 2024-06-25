use convert_case::{Case, Casing};
use snowman_connector::schema::{Column, Table};

use crate::{InsertTypedDictOptions, UpdateTypedDictOptions};

#[derive(Debug, Clone, Default)]
pub struct PydanticOptions {
    pub model_name_prefix: Option<String>,
    pub model_name_suffix: Option<String>,
}

impl PydanticOptions {
    pub fn make_class_name(&self, table_name: &str) -> String {
        let mut table_name = table_name.to_case(Case::Pascal);
        if let Some(prefix) = &self.model_name_prefix {
            table_name.insert_str(0, prefix);
        }
        if let Some(suffix) = &self.model_name_suffix {
            table_name.push_str(suffix);
        }
        table_name
    }
}

pub fn get_pydantic_modules() -> Vec<&'static str> {
    vec!["pydantic", "snowman"]
}

pub fn generate_pydantic_models(
    tables: &[Table],
    pydantic_options: &PydanticOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
) -> String {
    tables
        .iter()
        .map(|table| {
            generate_pydantic_model(
                table,
                pydantic_options,
                insert_typeddict_options,
                update_typeddict_options,
            )
        })
        .collect::<Vec<String>>()
        .join(
            "

",
        )
}

pub fn generate_pydantic_model(
    table: &Table,
    pydantic_options: &PydanticOptions,
    insert_typeddict_options: &InsertTypedDictOptions,
    update_typeddict_options: &UpdateTypedDictOptions,
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
    pydantic_schema.push_str(&format!(
        "class {}(pydantic.BaseModel, snowman.Table[\"{}\",\"{}\",]):\n",
        pydantic_options.make_class_name(&table.table_name),
        insert_typeddict_options.make_class_name(&table.table_name),
        update_typeddict_options.make_class_name(&table.table_name)
    ));
    if let Some(comment) = &table.comment {
        if !comment.is_empty() {
            pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
        }
    }

    pydantic_schema.push_str("    model_config = pydantic.ConfigDict(populate_by_name=True)\n");

    for column in &table.columns {
        let mut data_type = column.data_type.clone();
        if column.is_nullable {
            data_type.push_str(" | None");
        }
        let (field, has_default) = calc_pydantic_field(column);
        if has_default {
            pydantic_schema.push_str(&format!(
                "\n    {}: snowman.datatype.{} = {}\n",
                column.column_name.to_case(Case::Snake),
                data_type,
                field,
            ))
        } else {
            pydantic_schema.push_str(&format!(
                "\n    {}: typing.Annotated[snowman.datatype.{}, {},]\n",
                column.column_name.to_case(Case::Snake),
                data_type,
                field,
            ))
        };
        if let Some(comment) = column.comment.as_ref() {
            if !comment.is_empty() {
                pydantic_schema.push_str(&format!("    \"\"\"{}\"\"\"\n", comment));
            }
        }
    }
    pydantic_schema
}

enum Text {
    Quoted(String),
    Normal(String),
}

impl std::fmt::Display for Text {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Text::Quoted(text) => write!(f, "\"{}\"", text),
            Text::Normal(text) => write!(f, "{}", text),
        }
    }
}

impl<T: Into<String>> From<T> for Text {
    fn from(text: T) -> Self {
        Text::Normal(text.into())
    }
}

fn calc_pydantic_field(column: &Column) -> (String, bool) {
    let mut has_default = false;
    let mut args: Vec<(&str, Text)> = vec![];

    if let Some(comment) = column.comment.as_ref() {
        if !comment.is_empty() {
            args.push(("title", Text::Quoted(comment.to_string())));
        }
    }

    if column.column_name != column.column_name.to_case(Case::Snake) {
        args.push(("alias", Text::Quoted(column.column_name.clone())));
    }

    match column.default_value.as_deref() {
        Some("CURRENT_TIMESTAMP()") => {
            args.push((
                "default_factory",
                format!("snowman.datatype.{}.now", column.data_type).into(),
            ));
            has_default = true;
        }
        Some("CURRENT_DATE()") => {
            args.push((
                "default_factory",
                format!("snowman.datatype.{}.today", column.data_type).into(),
            ));
            has_default = true;
        }
        _ => {}
    }

    (
        format!(
            "pydantic.Field({})",
            args.iter()
                .map(|(k, v)| format!("{}={}", k, v))
                .collect::<Vec<String>>()
                .join(", "),
        ),
        has_default,
    )
}
