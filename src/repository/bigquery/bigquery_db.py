from google.cloud import bigquery
from flask import current_app as app, g
from mockfirestore import MockFirestore

from src.repository.bigquery.rejestrio import Rejestrio


def bigquery_db():
    """Singleton with db connection."""
    if 'bigquery' not in g:
        g.bigquery = BigQuery()
    return g.bigquery


def init_client():
    """Initialize db connection. Database is mocked for test purposes."""
    if app.config['ENV'] == 'test':
        # Mock bigquery - TODO
        return MockFirestore()
    return bigquery.Client(app.config['PROJECT_ID'])


class BigQuery:
    _instance = None

    def __init__(self):
        self._instance = init_client()
        self._rejestrio = Rejestrio(self._instance)

    def rejestrio(self):
        """Returns rejestrio collection interface."""
        return self._rejestrio

    def get_instance(self):
        """Returns google.cloud bigquery client instance for development purposes."""
        return self._instance
