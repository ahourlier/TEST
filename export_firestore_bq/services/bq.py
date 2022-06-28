from google.cloud import bigquery
import time
from google.cloud.exceptions import Conflict
import os

from config import BQ_DATASET


class BQService:
    def __init__(self) -> None:
        self.client = bigquery.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        self.dataset = self.client.dataset(BQ_DATASET)

    def create_table(self, table_name, schema):
        """
        Creates a table in BQ
        @params: table_name: Str name of the table
        @params: schema: List[dict] of all fields
        """
        # create table ref in dataset
        table_ref = self.dataset.table(table_name)
        # create table object
        table = bigquery.Table(table_ref, schema=schema)
        try:
            # try to create it
            table = self.client.create_table(table)
        except Conflict:
            # if already exists, delete it
            self.client.delete_table(table)
            # wait for 1s, just to be safe
            time.sleep(1)
            # try again to create it
            return self.create_table(table_name=table_name, schema=schema)
        return table

    def load_data_from_json(self, table, data, schema):
        """
        Load JSON data into BQ table
        @params: table: BQ Table object where to load data
        @params: data: Dict data to load
        @params: schema: List[dict] of all fields
        """
        # create job config to avoid schema errors
        job_config = bigquery.LoadJobConfig(schema=schema)
        # create job
        job = self.client.load_table_from_json(data, table, job_config=job_config)
        # trigger job checking for results
        try:
            job.result()
        except Exception as e:
            raise
        return
