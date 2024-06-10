use convert_case::{Case, Casing};

use snowman_connector::query::DatabaseSchema;

pub trait ToPython {
    fn database_module(&self) -> String;
    fn schema_module(&self) -> String;
    fn schema_file_path(&self) -> std::path::PathBuf;
}

impl ToPython for DatabaseSchema {
    fn database_module(&self) -> String {
        self.database_name.to_case(Case::Snake)
    }

    fn schema_module(&self) -> String {
        self.schema_name.to_case(Case::Snake)
    }

    fn schema_file_path(&self) -> std::path::PathBuf {
        std::path::PathBuf::from(format!("{}.py", self.schema_module()))
    }
}
