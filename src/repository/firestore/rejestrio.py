from dacite import from_dict
from flask import current_app as app
from src.models.krs_search_result import SearchResult
from src.models.rejestrio_record import RejestrIoRecord


class Rejestrio:
    _instance = None

    def __init__(self, instance):
        self._instance = instance
        self.search_limit = app.config['SEARCH_LIMIT']

    def insert(self, record):
        """Inserts rejestr.io krs record to the firebase."""
        if hasattr(record, 'krs'):
            document_id = record.krs
        else:
            document_id = record['krs']
        self._instance.collection(app.config["REJESTRIO_KRS_COLLECTION"]) \
            .document(document_id).set(record)

    def get_all(self):
        """Get all rejestr.io records from firebase"""
        docs = self._instance.collection(app.config["REJESTRIO_KRS_COLLECTION"]) \
            .stream()
        return SearchResult.from_stream(docs)

    def get_by_krs(self, krs):
        """Get rejestr.io record from firebase based on krs number"""
        return self.get_by_field('krs', krs)

    def get_by_field(self, field_name, query_to_search):
        """Get rejestr.io exactly one record from firebase based on field name"""
        docs = self._instance.collection(app.config["REJESTRIO_KRS_COLLECTION"]) \
            .where(field_name, u'==', query_to_search).stream()
        for doc in docs:
            return from_dict(data_class=RejestrIoRecord, data=doc.to_dict())

    def search_by_field(self, field_name, query_to_search):
        """Get rejestr.io records from firebase based on field_name set in app config,
        query and limited by search limit"""
        docs = self._instance.collection(app.config["REJESTRIO_KRS_COLLECTION"]) \
            .where(field_name, u'>=', query_to_search) \
            .where(field_name, u'<=', query_to_search + '\uf8ff') \
            .limit(self.search_limit) \
            .stream()
        return SearchResult.from_stream(docs)
