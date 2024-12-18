import functions_framework
from cloudevents.http import CloudEvent

from core.config import get_config
from core.schemas import (
    parse_data,
    DataSchema
)
from core.adapters.bigquery import BigQueryAdapter


@functions_framework.cloud_event
def main(cloud_event: CloudEvent):
    """
    Receive Data from Pub/Sub and Load to BigQuery

    Source: Pub/Sub
    Data: DataSchema (refer: ./core/schemas.py)
    """
    body_data = dict(cloud_event.data)
    data = parse_data(body_data, DataSchema)

    C = get_config()
    bq = BigQueryAdapter(C.BQ_PROJECT, C.BQ_DATASET)
    bq.load(data.data, data.table)

    return "OK"