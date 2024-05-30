from snowq.query import delete, insert, truncate, update

from snowq_sample.schema import cdp

if __name__ == "__main__":
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

    delete.from_(
        cdp.datalake.AdsDataHubData,
    ).where(
        "campaign_id = 1",
    )

    truncate.table.if_.exists(cdp.datalake.AdsDataHubData)
