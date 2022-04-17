import dataclasses

from dacite import from_dict
from flask import current_app as app
from src.models.user import User


class Users:
    _instance = None

    def __init__(self, instance):
        self._instance = instance

    def insert(self, record):
        """Inserts user record to the firebase."""
        self._instance.collection(app.config["USERS_COLLECTION"]) \
            .document(record.user_id).set(dataclasses.asdict(record))

    def get_by_id(self, user_id):
        """Get a user by id"""
        self.get_by_field('user_id', user_id)

    def get_by_field(self, field_name, query_to_search):
        """Get a user from firebase based on field name"""
        docs = self._instance.collection(app.config["USERS_COLLECTION"]) \
            .where(field_name, u'==', query_to_search).stream()
        for doc in docs:
            return from_dict(data_class=User, data=doc.to_dict())
