import dataclasses
import json
from src.models.krs_search_result import SearchEntity, SearchResult
from src.config import BaseConfig
from src.repository.firestore.firestore_db import firestore_db


def test_exact_name_search(client):
    expected_entity = SearchEntity(name="MBANKOWY", krs="74700060", nip="74700060")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/MBANKOWY")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_exact_krs_no(client):
    expected_entity = SearchEntity(name='BONUS BGC COMPANY', krs="123456789", nip="747096")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/123456789")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_partial_krs_no(client):
    expected_entity = SearchEntity(name='BONUS BGC COMPANY', krs="123456789", nip="987654321")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/1234567")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_exact_nip_no(client):
    expected_entity = SearchEntity(name='BONUS BGC COMPANY', krs="123456789", nip="987654321")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/987654321")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_partial_nip_no(client):
    expected_entity = SearchEntity(name='BONUS BGC COMPANY', krs="123456789", nip="987654321")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/9876543")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_lowercase(client):
    expected_entity = SearchEntity(name='BONUS BGC COMPANY', krs="123456789", nip="987654321")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/bonus%20bgc%20company")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_whitespace(client):
    expected_entity = SearchEntity(name='BONUS BGC COMPANY', krs="123456789", nip="987654321")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/bonus%20bgc")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_dash(client):
    expected_entity = SearchEntity(name='SIMPLIFY-COMPANY', krs="123456789", nip="987654321")
    expected_record = dataclasses.asdict(expected_entity)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/simplify-company")
    assert response.status_code == 200
    response_record = SearchResult.from_json(response.get_data(as_text=True))
    assert len(response_record.results) == 1
    assert response_record.results[0] == expected_entity


def test_many_results(client):
    for i in range(BaseConfig.SEARCH_LIMIT):
        expected_entity = SearchEntity(name=f'SIMPLIFY{i}', krs=f"12{i}789", nip=f"98{i}21")
        expected_record = dataclasses.asdict(expected_entity)
        firestore_db().rejestrio().insert(expected_record)
    response = client.get("/krs/search/simplify")
    assert response.status_code == 200
    response = response.data.decode('utf8')
    assert len(json.loads(response)['results']) == BaseConfig.SEARCH_LIMIT


def test_no_data_found(client):
    response = client.get("/krs/search/nodatafound")
    assert response.status_code == 200
    response = response.data.decode('utf8')
    assert json.loads(response) == dataclasses.asdict(SearchResult([]))
