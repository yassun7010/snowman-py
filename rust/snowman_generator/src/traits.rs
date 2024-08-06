use convert_case::{Case, Casing};

use snowman_connector::{query::DatabaseSchema, schema::Table};

pub trait ToPythonModule {
    fn database_module(&self) -> String;
    fn schema_module(&self) -> String;
}

impl ToPythonModule for DatabaseSchema {
    fn database_module(&self) -> String {
        self.database_name.to_case(Case::Snake)
    }

    fn schema_module(&self) -> String {
        self.schema_name.to_case(Case::Snake)
    }
}

impl ToPythonModule for Table {
    fn database_module(&self) -> String {
        self.database_name.to_case(Case::Snake)
    }

    fn schema_module(&self) -> String {
        self.schema_name.to_case(Case::Snake)
    }
}

pub trait ToPython: ToPythonModule {
    fn database_python_module_fullpath(
        &self,
        output_dirpath: &std::path::Path,
    ) -> std::path::PathBuf {
        output_dirpath
            .join(self.database_module())
            .join("__init__.py")
    }

    fn schema_python_typehint_fullpath(
        &self,
        output_dirpath: &std::path::Path,
    ) -> std::path::PathBuf {
        output_dirpath
            .join(self.database_module())
            .join(format!("_{}.py", self.schema_module()))
    }

    fn schema_python_code_fullpath(&self, output_dirpath: &std::path::Path) -> std::path::PathBuf {
        output_dirpath
            .join(self.database_module())
            .join(format!("{}.py", self.schema_module()))
    }
}

impl ToPython for DatabaseSchema {}

pub trait ToSQL {
    fn schema_sql_file_fullpath(&self, output_dirpath: &std::path::Path) -> std::path::PathBuf;
}

impl ToSQL for DatabaseSchema {
    fn schema_sql_file_fullpath(&self, output_dirpath: &std::path::Path) -> std::path::PathBuf {
        output_dirpath
            .join(self.database_module())
            .join(format!("{}.sql", self.schema_module()))
    }
}
