use clap::Args;

#[derive(Debug, Args)]
pub struct SchemaSync {}

pub async fn run_schema_sync_command(_: SchemaSync) -> Result<(), Box<dyn std::error::Error>> {
    let connection = snowq_connector::Connection::try_new_from_env()?;
    let tables =
        snowq_connector::query::schema_infomations::get_schema_infomations(&connection).await?;

    for table in tables {
        println!(
            "{}.{}.{}",
            table.database_name, table.schema_name, table.table_name
        );
        for column in table.columns {
            println!("    {}:{}", column.column_name, column.data_type);
        }
    }
    Ok(())
}
