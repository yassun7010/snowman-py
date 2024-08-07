use pretty_assertions::assert_eq;
use snowman_connector::{
    query::DatabaseSchema,
    schema::{Column, Table},
};
use snowman_generator::generate_schema_python_code;

#[tokio::test]
async fn test_generate_schema_python_code() {
    let database_schema = DatabaseSchema {
        database_name: "DATABASE".to_string(),
        schema_name: "SCHEMA".to_string(),
    };
    let tables = vec![Table {
        database_name: database_schema.database_name.clone(),
        schema_name: database_schema.schema_name.clone(),
        table_name: "USER".to_string(),
        comment: Some("User Table".to_string()),
        columns: vec![
            Column {
                column_name: "ID".to_string(),
                data_type: "INTEGER".to_string(),
                is_nullable: false,
                comment: Some("User ID".to_string()),
                default_value: None,
            },
            Column {
                column_name: "NAME".to_string(),
                data_type: "TEXT".to_string(),
                is_nullable: false,
                comment: Some("User Name".to_string()),
                default_value: None,
            },
            Column {
                column_name: "CREATED_AT".to_string(),
                data_type: "TIMESTAMP".to_string(),
                is_nullable: false,
                comment: Some("Created At".to_string()),
                default_value: Some("CURRENT_TIMESTAMP()".to_string()),
            },
        ],
    }];

    let code = generate_schema_python_code(
        &tables,
        &database_schema,
        &Default::default(),
        &Default::default(),
        &Default::default(),
        &Default::default(),
        &Default::default(),
    )
    .await
    .unwrap();

    assert_eq!(
        code,
        r#"
#
# Code generated by snowman; DO NOT EDIT.
#
# For more information about snowman,
# please refer to https://github.com/yassun7010/snowman-py .
#

import datetime
import pydantic
import snowman
import typing
import zoneinfo

if typing.TYPE_CHECKING:
    from . import _schema as _schema

# TABLE: DATABASE.SCHEMA.USER
@snowman.table("DATABASE", "SCHEMA", "USER")
class User(pydantic.BaseModel, snowman.Table["_schema._UserInsertTypedDict","_schema._UserUpdateTypedDict",]):
    """User Table"""
    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: typing.Annotated[snowman.datatype.INTEGER, pydantic.Field(title="User ID", alias="ID"),]
    """User ID"""

    name: typing.Annotated[snowman.datatype.TEXT, pydantic.Field(title="User Name", alias="NAME"),]
    """User Name"""

    created_at: typing.Annotated[snowman.datatype.TIMESTAMP, pydantic.Field(title="Created At", alias="CREATED_AT"),] = snowman.pydantic.DefaultFactory(lambda: datetime.datetime.now(datetime.UTC))
    """Created At"""
"#
        .strip_prefix('\n')
        .unwrap()
    )
}

#[tokio::test]
async fn test_generate_schema_python_code_of_empty_columns_table() {
    let database_schema = DatabaseSchema {
        database_name: "DATABASE".to_string(),
        schema_name: "SCHEMA".to_string(),
    };
    let tables = vec![Table {
        database_name: database_schema.database_name.clone(),
        schema_name: database_schema.schema_name.clone(),
        table_name: "USER".to_string(),
        comment: Some("User Table".to_string()),
        columns: vec![],
    }];

    let code = generate_schema_python_code(
        &tables,
        &database_schema,
        &Default::default(),
        &Default::default(),
        &Default::default(),
        &Default::default(),
        &Default::default(),
    )
    .await
    .unwrap();

    assert_eq!(
        code,
        r#"
#
# Code generated by snowman; DO NOT EDIT.
#
# For more information about snowman,
# please refer to https://github.com/yassun7010/snowman-py .
#

import datetime
import pydantic
import snowman
import typing
import zoneinfo

if typing.TYPE_CHECKING:
    from . import _schema as _schema

# TABLE: DATABASE.SCHEMA.USER
@snowman.table("DATABASE", "SCHEMA", "USER")
class User(pydantic.BaseModel, snowman.Table["_schema._UserInsertTypedDict","_schema._UserUpdateTypedDict",]):
    """User Table"""
    model_config = pydantic.ConfigDict(populate_by_name=True)
"#
        .strip_prefix('\n')
        .unwrap()
    )
}
