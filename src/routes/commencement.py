from flask import Blueprint

from src.repository.firestore.firestore_db import firestore_db
from src.service import commencement

GET_COMMENCEMENT = Blueprint('commencement', __name__, url_prefix='/get_commencement')


@GET_COMMENCEMENT.route("/")
def hello():
    """Greetings endpoint."""
    return "Hello Commencement!"


@GET_COMMENCEMENT.route('/<string:krs_no>')
def results(krs_no):
    """Get RejestrIoRecord instance based on provided krs_no."""
    krs_record = firestore_db().rejestrio().get_by_krs(krs_no)
    commencement_text = commencement.from_krs_record(krs_record)
    return f'{commencement_text}'
