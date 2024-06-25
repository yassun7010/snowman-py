use std::{path::PathBuf, str::FromStr};

use snowman_connector::{
    query::DatabaseSchema,
    schema::{Column, Table},
};
use snowman_generator::generate_schema_python_code;

#[tokio::main]
async fn main() {
    let database_schema = DatabaseSchema {
        database_name: "DATABASE".to_string(),
        schema_name: "SCHEMA".to_string(),
    };
    let tables = vec![Table {
        database_name: database_schema.database_name,
        schema_name: database_schema.schema_name,
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

    let output_dir = PathBuf::from_str(&std::env::args().nth(1).unwrap()).unwrap();

    // SQL Code.
    std::fs::write(
        output_dir.join("model_schema.sql"),
        tables
            .iter()
            .map(snowman_generator::generate_sql_definition)
            .collect::<Vec<String>>()
            .join("\n\n"),
    )
    .unwrap();

    // Pydantic Model Code.
    std::fs::write(
        output_dir.join("model_generate.py"),
        generate_schema_python_code(
            &tables,
            &Default::default(),
            &Default::default(),
            &Default::default(),
        )
        .await
        .unwrap(),
    )
    .unwrap();
}
