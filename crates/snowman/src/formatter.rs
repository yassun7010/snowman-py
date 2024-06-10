pub fn run_ruff_format_if_exists(output_dirpath: &std::path::Path) {
    // if ruff command found in local machine, run it on output_dirpath
    match std::process::Command::new("ruff")
        .arg("format")
        .arg(output_dirpath)
        .output()
    {
        Ok(_) => {}
        Err(err) => {
            if err.kind() == std::io::ErrorKind::NotFound {
                return;
            }
            eprintln!("ruff command not found: {}", err);
        }
    }
}
