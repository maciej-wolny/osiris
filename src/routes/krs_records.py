import random
import time

import requests
from elasticsearch import Elasticsearch
from flask import Blueprint
from flask import current_app as app
from google.cloud import secretmanager

from src.models.krs_record import KRSRecord
from src.models.krs_search_result import SearchResult
from src.repository.firestore.firestore_db import firestore_db
from src.service.search import generate_query

KRS_RECORDS = Blueprint('krs_records', __name__, url_prefix='/krs')
COLORS = ['red', 'green', 'blue']

cloud_id = "search-devint:ZXVyb3BlLXdlc3QzLmdjcC5jbG91ZC5lcy5pbyQ4MGIxN2YzYzIwNzk0YWJhODA2NjRmNjQ5MDNlYjk0YiQ3M2ZjMmM4YzRjOWI0YzJjYTdjYzIyNjhiYTdmNDVmYg=="
secret_id = 'projects/294333038581/secrets/elastic-devint/versions/1'
client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(secret_id)
passwrd = response.payload.data.decode('UTF-8')

es = Elasticsearch(
    cloud_id=cloud_id,
    http_auth=('elastic', passwrd),
)


@KRS_RECORDS.route("/")
def hello():
    """Greetings endpoint."""
    return "Hello GLH"


@KRS_RECORDS.route('/fetchData')
def fetch_krs_data():
    """Meant for periodical execution. Downloads the data
    from krs database and stores it in firebase"""
    for page_index in range(1, 10):
        record_list = get_rejestrio_krs_records(page_index)
        for record in record_list:
            firestore_db().rejestrio().insert(record)


@KRS_RECORDS.route('/insertRandom/<document>')
def insert_random(document):
    """Inserts random KRSRecord to firebase"""
    record = KRSRecord(address_city=random.choice(COLORS),
                       address_code=random.choice(COLORS),
                       address_house_no=random.choice(COLORS),
                       address_street=random.choice(COLORS),
                       district_court=random.choice(COLORS),
                       krs=document,
                       name=random.choice(COLORS),
                       nip=random.choice(COLORS),
                       regon=random.choice(COLORS),
                       shared_capital=random.choice(COLORS))
    firestore_db().krs().insert(record)
    return "ok"


@KRS_RECORDS.route('/search/')
def handle_empty_search():
    return ""


@KRS_RECORDS.route('/search/<prefix>')
def get_by_name_prefix(prefix):
    """Gets KRSRecord from firestore by name prefix"""
    if len(prefix) < 3:
        return ""

    query = generate_query(prefix)
    start = time.time()
    res = es.search(index='one-more-test', body={"query": query})
    end = time.time()
    # print("took {}".format(end - start))
    # print("res {}".format(res))
    return res['hits']


def get_rejestrio_krs_records(page):
    """Get 100 records from rejestr.io api from a corresponding page.
    Records are sorted by kapital."""
    krs_search_url = app.config['REJESTR_IO_BASE_URL'] + '/krs'
    krs_search_headers = {'Authorization': app.config['REJESTR_IO_KEY']}
    krs_search_params = {'sort': 'kapital:desc',
                         'page': page,
                         'per_page': 100}
    response = requests.get(url=krs_search_url,
                            headers=krs_search_headers,
                            params=krs_search_params)
    data = response.json()
    return data['items']
