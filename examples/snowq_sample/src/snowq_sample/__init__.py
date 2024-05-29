from snowq.query import insert, update

from snowq_sample.schema import cdp

insert.into(
    cdp.datalake.AdsDataHubData,
).values(
    cdp.datalake.AdsDataHubData.model_validate({}),
)

update(
    cdp.datalake.AdsDataHubData,
).set(
    {"campaign_id": "1234"},
).where(
    "campaign_id = 1",
)
