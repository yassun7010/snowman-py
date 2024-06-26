use crate::Parameters;

pub async fn get_parameters() -> Result<Parameters, crate::Error> {
    Ok(Parameters::default())
}
