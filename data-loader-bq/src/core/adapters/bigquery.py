from typing import List

from pydantic import BaseModel
from google.cloud.bigquery import Client as BigQueryClient


class BigQueryAdapter:
    """
    BigQuery Adapter

    Adapter for loading data to BigQuery.

    params:
        - project: [str]. Project ID for BigQuery
    """
    __bq: BigQueryClient
    __dataset: str

    def __init__(self, project_id: str, dataset: str):
        self.__bq = BigQueryClient(project_id)
        self.__dataset = dataset


    def load(self, data: BaseModel, tablename: str):
        """
        Load

        Load data from model to BigQuery.

        params:
            - data: List[BaseModel] List of data model to be loaded.
            - dataset: str. Dataset for BQ Table.
        """
        full_tablename = f"{self.__dataset}.{tablename}"
        table = self.__bq.get_table(full_tablename)
        self.__bq.insert_rows_json(table, [data.model_dump()])
