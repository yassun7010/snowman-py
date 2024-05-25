import snowq

from snowq_sample.schema import cdp

snowq.query.insert.into(cdp.datalake.AdsDataHubData).values(
    cdp.datalake.AdsDataHubData.model_validate({})
)
