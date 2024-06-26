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
        pydantic_schema.push_str(&format!("\n    {}", generate_column(column)));

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

enum PydanticDefault {
    None,
    Default(Text),
    DefaultFactory,
}

fn generate_column(column: &Column) -> String {
    let mut data_type = column.data_type.clone();
    if column.is_nullable {
        data_type.push_str(" | None");
    }

    let mut args: Vec<(&str, Text)> = vec![];

    if let Some(comment) = column.comment.as_ref() {
        if !comment.is_empty() {
            args.push(("title", Text::Quoted(comment.to_string())));
        }
    }

    if column.column_name != column.column_name.to_case(Case::Snake) {
        args.push(("alias", Text::Quoted(column.column_name.clone())));
    }

    let default = match column.default_value.as_deref() {
        // NULL
        Some("NULL") => PydanticDefault::Default("None".into()),
        // BOOLEAN
        Some("TRUE") => PydanticDefault::Default("True".into()),
        Some("FALSE") => PydanticDefault::Default("False".into()),
        // TIMESTAMP
        Some("CURRENT_TIMESTAMP()") => {
            args.push((
                "default_factory",
                format!("snowman.datatype.{}.now", column.data_type).into(),
            ));
            PydanticDefault::DefaultFactory
        }
        // DATE
        Some("CURRENT_DATE()") => {
            args.push((
                "default_factory",
                format!("snowman.datatype.{}.today", column.data_type).into(),
            ));
            PydanticDefault::DefaultFactory
        }
        Some(default_value) => {
            // STRING
            if ["VARCHAR", "CHAR", "CHARACTER", "STRING", "TEXT"]
                .contains(&column.data_type.as_str())
                && default_value.starts_with('\'')
                && default_value.ends_with('\'')
            {
                PydanticDefault::Default(Text::Quoted(
                    default_value[1..default_value.len() - 1].replace('"', "\\\""),
                ))
            }
            // INTEGER
            else if let Ok(default_value) = default_value.parse::<i64>() {
                PydanticDefault::Default(default_value.to_string().into())
            }
            // FLOAT
            else if let Ok(default_value) = default_value.parse::<f64>() {
                PydanticDefault::Default(default_value.to_string().into())
            }
            // UNKNOWN
            else {
                PydanticDefault::None
            }
        }
        // UNKNOWN
        None => PydanticDefault::None,
    };

    let field = format!(
        "pydantic.Field({})",
        args.iter()
            .map(|(k, v)| format!("{}={}", k, v))
            .collect::<Vec<String>>()
            .join(", "),
    );

    match default {
        PydanticDefault::None => format!(
            "{}: typing.Annotated[snowman.datatype.{}, {},]\n",
            column.column_name.to_case(Case::Snake),
            data_type,
            field,
        ),
        PydanticDefault::Default(default) => format!(
            "{}: typing.Annotated[snowman.datatype.{}, {},] = {}\n",
            column.column_name.to_case(Case::Snake),
            data_type,
            field,
            default,
        ),
        PydanticDefault::DefaultFactory => format!(
            "{}: snowman.datatype.{} = {}\n",
            column.column_name.to_case(Case::Snake),
            data_type,
            field,
        ),
    }
}

#[cfg(test)]
mod test {
    use pretty_assertions::assert_eq;
    use snowman_connector::schema::Column;

    use crate::model::pydantic::generate_column;

    #[test]
    fn test_generate_column_by_null_default() {
        let column = Column {
            column_name: "ID".to_string(),
            data_type: "INTEGER".to_string(),
            is_nullable: true,
            comment: Some("User ID".to_string()),
            default_value: Some("NULL".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"id: typing.Annotated[snowman.datatype.INTEGER | None, pydantic.Field(title="User ID", alias="ID"),] = None
"#
        );
    }

    #[test]
    fn test_generate_column_by_true_default() {
        let column = Column {
            column_name: "IS_ACTIVE".to_string(),
            data_type: "BOOLEAN".to_string(),
            is_nullable: false,
            comment: Some("Is Active".to_string()),
            default_value: Some("TRUE".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"is_active: typing.Annotated[snowman.datatype.BOOLEAN, pydantic.Field(title="Is Active", alias="IS_ACTIVE"),] = True
"#
        );
    }

    #[test]
    fn test_generate_column_by_false_default() {
        let column = Column {
            column_name: "IS_ACTIVE".to_string(),
            data_type: "BOOLEAN".to_string(),
            is_nullable: false,
            comment: Some("Is Active".to_string()),
            default_value: Some("FALSE".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"is_active: typing.Annotated[snowman.datatype.BOOLEAN, pydantic.Field(title="Is Active", alias="IS_ACTIVE"),] = False
"#
        );
    }

    #[test]
    fn test_generate_column_by_current_timestamp_default() {
        let column = Column {
            column_name: "CREATED_AT".to_string(),
            data_type: "TIMESTAMP".to_string(),
            is_nullable: false,
            comment: Some("Created At".to_string()),
            default_value: Some("CURRENT_TIMESTAMP()".to_string()),
        };

        let result = super::generate_column(&column);
        assert_eq!(
            result,
            r#"created_at: snowman.datatype.TIMESTAMP = pydantic.Field(title="Created At", alias="CREATED_AT", default_factory=snowman.datatype.TIMESTAMP.now)
"#
        );
    }

    #[test]
    fn test_generate_column_by_current_date_default() {
        let column = Column {
            column_name: "CREATED_AT".to_string(),
            data_type: "DATE".to_string(),
            is_nullable: false,
            comment: Some("Created At".to_string()),
            default_value: Some("CURRENT_DATE()".to_string()),
        };

        let result = super::generate_column(&column);
        assert_eq!(
            result,
            r#"created_at: snowman.datatype.DATE = pydantic.Field(title="Created At", alias="CREATED_AT", default_factory=snowman.datatype.DATE.today)
"#
        );
    }

    #[test]
    fn test_generate_column_by_string_default() {
        let column = Column {
            column_name: "NAME".to_string(),
            data_type: "TEXT".to_string(),
            is_nullable: false,
            comment: Some("Name".to_string()),
            default_value: Some("'John Doe'".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"name: typing.Annotated[snowman.datatype.TEXT, pydantic.Field(title="Name", alias="NAME"),] = "John Doe"
"#
        );
    }

    #[test]
    fn test_generate_column_by_double_quoted_string_default() {
        let column = Column {
            column_name: "COMMENT".to_string(),
            data_type: "TEXT".to_string(),
            is_nullable: false,
            comment: Some("Name".to_string()),
            default_value: Some("'He said. \"Hello.\"'".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"comment: typing.Annotated[snowman.datatype.TEXT, pydantic.Field(title="Name", alias="COMMENT"),] = "He said. \"Hello.\""
"#
        );
    }

    #[test]
    fn test_generate_column_by_integer_default() {
        let column = Column {
            column_name: "AGE".to_string(),
            data_type: "INTEGER".to_string(),
            is_nullable: false,
            comment: Some("Age".to_string()),
            default_value: Some("20".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"age: typing.Annotated[snowman.datatype.INTEGER, pydantic.Field(title="Age", alias="AGE"),] = 20
"#
        );
    }

    #[test]
    fn test_generate_column_by_float_default() {
        let column = Column {
            column_name: "HEIGHT".to_string(),
            data_type: "FLOAT".to_string(),
            is_nullable: false,
            comment: Some("Height".to_string()),
            default_value: Some("170.5".to_string()),
        };

        let result = generate_column(&column);
        assert_eq!(
            result,
            r#"height: typing.Annotated[snowman.datatype.FLOAT, pydantic.Field(title="Height", alias="HEIGHT"),] = 170.5
"#
        );
    }
}
