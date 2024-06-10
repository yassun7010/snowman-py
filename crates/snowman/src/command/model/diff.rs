use std::io::Write;

use crate::{
    config::{get_model_output_dirpath, get_pydantic_options, get_snowflake_connection},
    database::fetch_database_schemas,
    formatter::run_ruff_format_if_exists,
};
use console::{style, Style};
use similar::{ChangeTag, TextDiff};
use snowman_generator::ToPython;

struct Line(Option<usize>);

impl std::fmt::Display for Line {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self.0 {
            None => write!(f, "    "),
            Some(idx) => write!(f, "{:<4}", idx + 1),
        }
    }
}
#[derive(clap::Args)]
pub struct Args {
    #[arg(long)]
    pub output_dir: Option<std::path::PathBuf>,
}

pub async fn run(args: Args) -> Result<(), anyhow::Error> {
    let config_source = snowman_config::find_path()?;
    let config = snowman_config::load_from_source(&config_source)?;
    let connection = get_snowflake_connection(&config)?;

    let insert_typeddict_options = snowman_generator::InsertTypedDictOptions::default();
    let update_typeddict_options = snowman_generator::UpdateTypedDictOptions::default();
    let pydantic_options = get_pydantic_options(&config);

    let output_dirpath = &config_source.as_ref().parent().unwrap().join(
        args.output_dir
            .unwrap_or_else(|| get_model_output_dirpath(&config)),
    );

    let schemas = fetch_database_schemas(&connection, &config).await?;

    let sources = futures::future::try_join_all(schemas.iter().map(|schema| async {
        snowman_generator::generate_schema_python_code(
            &connection,
            schema,
            &pydantic_options,
            &insert_typeddict_options,
            &update_typeddict_options,
        )
        .await
    }))
    .await?;

    // zip database_schema and sources and print diff
    schemas
        .iter()
        .zip(sources.into_iter())
        .try_for_each(|(schema, mut new)| {
            let old = std::fs::read_to_string(
                output_dirpath
                    .join(schema.database_module())
                    .join(schema.schema_file_path()),
            )
            .unwrap_or("".to_string());

            if !old.is_empty() {
                // write tmp file and format by ruff and get formatted code string.
                // tmp file remove auto.
                let mut file = tempfile::NamedTempFile::new()?;
                file.write_all(new.as_bytes())?;
                run_ruff_format_if_exists(file.path());
                new = std::fs::read_to_string(file.path())?;
            }

            let diff = TextDiff::from_lines(&old, &new);
            for (idx, group) in diff.grouped_ops(3).iter().enumerate() {
                if idx > 0 {
                    println!("{:-^1$}", "-", 80);
                }
                for op in group {
                    for change in diff.iter_inline_changes(op) {
                        let (sign, s) = match change.tag() {
                            ChangeTag::Delete => ("-", Style::new().red()),
                            ChangeTag::Insert => ("+", Style::new().green()),
                            ChangeTag::Equal => (" ", Style::new().dim()),
                        };
                        print!(
                            "{}{} |{}",
                            style(Line(change.old_index())).dim(),
                            style(Line(change.new_index())).dim(),
                            s.apply_to(sign).bold(),
                        );
                        for (emphasized, value) in change.iter_strings_lossy() {
                            if emphasized {
                                print!("{}", s.apply_to(value).underlined().on_black());
                            } else {
                                print!("{}", s.apply_to(value));
                            }
                        }
                        if change.missing_newline() {
                            println!();
                        }
                    }
                }
            }

            Ok::<(), anyhow::Error>(())
        })?;

    Ok(())
}
