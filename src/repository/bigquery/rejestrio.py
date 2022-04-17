from flask import current_app as app
from google.cloud import bigquery

from src.models.schema.rejestrio import REJESTRIO_SCHEMA
from src.repository.bigquery.utils import table_exist


class Rejestrio:
    _instance = None

    def __init__(self, instance):
        self._instance = instance
        self.table_id = "{}.{}".format(app.config['PROJECT_ID'],
                                       app.config['REJESTRIO_DATASET_ID'])

    def create_if_not_exist(self):
        """Creates BigQuery table if it does not exist."""
        if not table_exist(self._instance, self.table_id):
            table = bigquery.Table(self.table_id, schema=REJESTRIO_SCHEMA)
            self._instance.create_table(table)

    def get_last_date(self):
        """Queries BQ to check for last first_entry_date within already inserted data."""
        query_content = ('SELECT MAX(first_entry_date) '
                         'FROM `{}`'.format(self.table_id))
        query_job = self._instance.query(query_content)
        rows = query_job.result()
        if rows.total_rows == 0:
            return None
        return rows.to_dataframe().iloc[0][0]
