pub fn run_ruff_format_if_exists(output_dirpath: &std::path::Path) -> Result<(), std::io::Error> {
    // For import sorting.
    // See https://github.com/astral-sh/ruff/issues/8367#issuecomment-1850317629
    if let Err(err) = std::process::Command::new("ruff")
        .arg("check")
        .arg("--select")
        .arg("I")
        .arg("--fix")
        .arg(output_dirpath)
        .output()
    {
        // Skip if ruff command is not found.
        if err.kind() == std::io::ErrorKind::NotFound {
            return Ok(());
        }
        return Err(err);
    };

    std::process::Command::new("ruff")
        .arg("format")
        .arg(output_dirpath)
        .output()?;

    Ok(())
}
