# pylint: disable=R0903
# rules irrelevant for config
import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    # firestore
    PROJECT_ID = "simplify-docs"
    # firestore
    KRS_COLLECTION = "krs-devint"
    REJESTRIO_KRS_COLLECTION = "rejestrio-krs-devint"
    CEIDG_COLLECTION = "ceidg-krs-devint"
    REJESTRIO_KRS_COLLECTION = "rejestrio-prod"
    USERS_COLLECTION = "users-devint"
    REJESTR_IO_BASE_URL = "https://rejestr.io/api/v1"
    REJESTR_IO_KEY = "44a55992-e9a2-4d6e-91f8-eb134524306f"
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = "simplify.log"
    SEARCH_LIMIT = 20
    QUERIED_FIELD_NAMES = ['name', 'krs', 'nip']

    # bigquery
    REJESTRIO_DATASET_ID = "simplify_docs_prod.krs_devint"

    # ApiRegon
    API_REGON_BASE_URL = 'https://wyszukiwarkaregon.stat.gov.pl/wsBIR/wsdl/' \
                         'UslugaBIRzewnPubl-ver11-prod.wsdl'
    API_REGON_TOKEN = 'bec4a0d036174eb488fb'
    # ApiCEIDG
    API_CEIDG_URL = 'https://datastore.ceidg.gov.pl/CEIDG.DataStore/services/' \
                    'DataStoreProvider201901.svc?wsdl'
    API_CEIDG_TOKEN = '9MEGSBAE0dU5U6PlS9uJnQmEPJabgsbzn9Hkj+4UWKlb88InD1OYWE' \
                      'C74ZW3TDFR'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = "dev"


class TestConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    ENV = "test"
    FIRESTORE_KRS_COLLECTION = "krs-test"
    REJESTRIO_KRS_COLLECTION = "rejestrio-krs-test"
    USERS_COLLECTION = "users-test"
    CEIDG_COLLECTION = "ceidg-krs-test"
    REJESTRIO_DATASET_ID = "krs-test"
    LOGGING_LOCATION = "tests.log"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = "prod"
    FIRESTORE_KRS_COLLECTION = "krs-prod"
    REJESTRIO_KRS_COLLECTION = "rejestrio-krs-prod"
    CEIDG_COLLECTION = "ceidg-krs-prod"
    REJESTRIO_DATASET_ID = "simplify_docs_prod.rejestrio_prod"
    REJESTRIO_KRS_COLLECTION = "rejestrio-prod"
    USERS_COLLECTION = "users-prod"


CONFIG = {
    "dev": "src.config.DevelopmentConfig",
    "test": "src.config.TestConfig",
    "prod": "src.config.ProductionConfig",
    "default": "src.config.DevelopmentConfig",
}


def configure_app(app):
    """Initializes configuration for flask app."""
    config_name = os.getenv("FLASK_CONFIGURATION", "default")
    app.config.from_object(CONFIG[config_name])
