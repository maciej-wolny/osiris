from flask import current_app as app

from src.models.krs_search_result import SearchResult


class CEIDG:
    _instance = None

    def __init__(self, instance):
        self._instance = instance

    def insert(self, record):
        """Inserts ceidg record to the firebase."""
        self._instance.collection(app.config["CEIDG_COLLECTION"]) \
            .document(record['DanePodstawowe']['REGON']).set(record)

    def get_all(self):
        """Get all krs records from firebase."""
        docs = self._instance.collection(app.config["REJESTRIO_KRS_COLLECTION"]) \
            .stream()
        return SearchResult.from_stream(docs)
