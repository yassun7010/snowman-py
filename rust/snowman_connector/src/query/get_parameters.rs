use crate::{Connection, Parameters};

pub async fn get_parameters(connection: &Connection) -> Result<Parameters, crate::Error> {
    let rows = connection.execute("SHOW PARAMETERS").await?;
    let mut timezone = "America/Los_Angeles".to_string(); // Default timezone
    let mut timestamp_type_mapping = "TIMESTAMP_NTZ".to_string(); // Default timestamp type mapping

    for row in rows.iter() {
        let name = row.get::<String>("key").unwrap();
        let value = row.get::<String>("value").unwrap();
        match (name.as_str(), value.as_str()) {
            (_, "") => {}
            ("TIMEZONE", value) => timezone = value.to_string(),
            ("TIMESTAMP_TYPE_MAPPING", value) => timestamp_type_mapping = value.to_string(),
            _ => {}
        }
    }

    Ok(Parameters {
        timezone,
        timestamp_type_mapping,
    })
}
