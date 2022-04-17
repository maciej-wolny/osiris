import ast
import dataclasses
import json

import pytest
from dacite import from_dict
from tests import commencement_utils as utils

from src.models.rejestrio_record import RejestrIoRecord
from src.repository.firestore.firestore_db import firestore_db
from src.service.commencement import LEGAL_FORMS_DICT, from_krs_record


def test_hello(client):
    response = client.get("/get_commencement/")
    assert response.status_code == 200 and response.get_data(
        as_text=True) == "Hello Commencement!"


@pytest.mark.parametrize(
    "legal_form",
    list(LEGAL_FORMS_DICT),
    ids=list(LEGAL_FORMS_DICT))
def test_create_commencement_every_function(client, legal_form):
    results = utils.create_results(legal_form)
    expected_entity = from_dict(data_class=RejestrIoRecord, data=results)
    expected_record = dataclasses.asdict(expected_entity)
    expected_commencement = from_krs_record(expected_entity)
    expected_commencement = ast.literal_eval(expected_commencement)
    firestore_db().rejestrio().insert(expected_record)
    response = client.get(f"/get_commencement/{results['krs']}")
    assert response.status_code == 200
    response = response.data.decode('utf8')
    assert expected_commencement['results'] == json.loads(response)['results']
