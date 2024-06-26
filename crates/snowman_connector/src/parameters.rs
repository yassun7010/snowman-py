pub struct Parameters {
    pub timezone: String,
    pub timestamp_type_mapping: String,
}

impl Default for Parameters {
    fn default() -> Self {
        Self {
            timezone: "America/Los_Angeles".to_string(),
            timestamp_type_mapping: "TIMESTAMP_NTZ".to_string(),
        }
    }
}
