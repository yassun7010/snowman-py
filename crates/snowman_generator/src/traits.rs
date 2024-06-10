use convert_case::{Case, Casing};

use snowman_connector::query::DatabaseSchema;

pub trait ToPython {
    fn database_module(&self) -> String;
    fn schema_module(&self) -> String;
    fn schema_file_fullpath(&self, output_dirpath: &std::path::Path) -> std::path::PathBuf;
}

impl ToPython for DatabaseSchema {
    fn database_module(&self) -> String {
        self.database_name.to_case(Case::Snake)
    }

    fn schema_module(&self) -> String {
        self.schema_name.to_case(Case::Snake)
    }

    fn schema_file_fullpath(&self, output_dirpath: &std::path::Path) -> std::path::PathBuf {
        output_dirpath
            .join(self.database_module())
            .join(format!("{}.py", self.schema_module()))
    }
}
