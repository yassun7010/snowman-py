use std::{path::PathBuf, str::FromStr};

use snowman_connector::{
    query::DatabaseSchema,
    schema::{Column, Table},
};
use snowman_generator::{
    formatter::run_ruff_format_if_exists, generate_schema_python_code,
    generate_schema_python_typehint,
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let database_schema = DatabaseSchema {
        database_name: "DATABASE".to_string(),
        schema_name: "SCHEMA".to_string(),
    };

    let tables = vec![Table {
        table_type: "BASE TABLE".to_string(),
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
                column_name: "AGE".to_string(),
                data_type: "INTEGER".to_string(),
                is_nullable: true,
                comment: Some("User Age".to_string()),
                default_value: Some("NULL".to_string()),
            },
            Column {
                column_name: "CREATED_AT".to_string(),
                data_type: "TIMESTAMP_TZ".to_string(),
                is_nullable: false,
                comment: Some("Created At".to_string()),
                default_value: Some("CURRENT_TIMESTAMP()".to_string()),
            },
        ],
    }];

    let output_dir =
        PathBuf::from_str(&std::env::args().nth(1).expect("need output_dirpath arg."))?;

    // SQL Code.
    std::fs::write(
        output_dir.join("your/database/schema.sql"),
        tables
            .iter()
            .map(snowman_generator::generate_sql_definition)
            .collect::<Vec<String>>()
            .join("\n\n"),
    )?;

    // Pydantic Model Code.
    std::fs::write(
        output_dir.join("your/database/_schema.py"),
        generate_schema_python_typehint(
            &tables,
            &[],
            &Default::default(),
            &Default::default(),
            &Default::default(),
        )
        .await?,
    )?;

    std::fs::write(
        output_dir.join("your/database/schema.py"),
        generate_schema_python_code(
            &tables,
            &[],
            &database_schema,
            &Default::default(),
            &Default::default(),
        )
        .await?,
    )?;

    run_ruff_format_if_exists(&output_dir)?;

    Ok(())
}
