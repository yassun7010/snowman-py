import snowq

from snowq_sample.schema import cdp

snowq.query.insert.into(cdp.datalake.AdsDataHubData).values(
    cdp.datalake.AdsDataHubData.model_validate({})
)

snowq.query.update(cdp.datalake.AdsDataHubData).set({"campaign_id": "1234"}).where(
    "campaign_id = 1"
)
