from google.cloud import firestore
from flask import current_app as app, g
from mockfirestore import MockFirestore

from src.repository.firestore.ceidg import CEIDG
from src.repository.firestore.krs import Krs
from src.repository.firestore.rejestrio import Rejestrio
from src.repository.users import Users


def firestore_db():
    """Singleton with db connection."""
    if 'firestore' not in g:
        g.firestore = Firestore()
    return g.firestore


def init_client():
    """Initialize db connection. Database is mocked for test purposes."""
    if app.config['ENV'] == 'test':
        return MockFirestore()
    return firestore.Client(app.config['PROJECT_ID'])


class Firestore:
    _instance = None

    def __init__(self):
        self._instance = init_client()
        self._rejestrio = Rejestrio(self._instance)
        self._krs = Krs(self._instance)
        self._ceidg = CEIDG(self._instance)
        self._users = Users(self._instance)

    def rejestrio(self):
        """Returns rejestrio collection interface."""
        return self._rejestrio

    def krs(self):
        """Returns krs collection interface."""
        return self._krs

    def ceidg(self):
        """Returns ceidg collection interface."""
        return self._ceidg

    def users(self):
        """Returns users collection interface."""
        return self._users

    def get_instance(self):
        """Returns google.cloud firestore instance for development purposes."""
        return self._instance
