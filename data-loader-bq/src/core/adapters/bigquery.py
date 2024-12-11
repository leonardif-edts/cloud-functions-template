from typing import List

from pydantic import BaseModel
from google.cloud.bigquery import Client as BigQueryClient


MERGE_QUERY = """
MERGE INTO 
"""


class BigQueryAdapter:
    """
    BigQuery Adapter

    Adapter for loading data to BigQuery.

    params:
        - project: [str]. Project ID for BigQuery
    """
    __bq: BigQueryClient

    def __init__(self, project_id: str):
        self.__bq = BigQueryClient(project_id)


    def load(self, data: BaseModel, tablename: str):
        """
        Load

        Load data from model to BigQuery.

        params:
            - data: List[BaseModel] List of data model to be loaded.
            - tablename: str. Dataset and tablename for BQ (format: dataset.tablename)
        """
        json_rows = [data.model_dump()]
        table = self.__bq.get_table(tablename)
        self.__bq.insert_rows(table, json_rows)
