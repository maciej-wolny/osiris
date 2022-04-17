import threading
import time

from flask import Blueprint
from flask import current_app as app
from src.processing.krs_etl import KrsEtl, log_execution_time, log_message
from src.repository.bigquery.bigquery_db import bigquery_db

TRIGGER = Blueprint('trigger', __name__, url_prefix='/trigger')


@TRIGGER.route('/fetch_rejestrio')
def fetch_krs_data():
    """Endpoint to be ran whenever new krs data needs to be ingested. Gets data from rejestr.io for
    dates that are not in BigQuery and inserts the acquired data. Multi-threading utilized for
    inserting."""
    bigquery_db().rejestrio().create_if_not_exist()
    last_date = bigquery_db().rejestrio().get_last_date()

    thread = threading.Thread(target=start_rejestrio_job,
                              args=(last_date,
                                    app.config['PROJECT_ID'],
                                    app.config['REJESTRIO_DATASET_ID'],))
    thread.daemon = True
    thread.start()
    return "Job submitted"


def start_rejestrio_job(last_date, project_id, dataset_id):
    """Method that allows rejestrio job to run in the background"""
    threads_count = 8
    if last_date is None:
        log_message('Dupa blada nie ma danych w bazie.')
        return
    etl = KrsEtl(start_date=last_date,
                 project_id=project_id,
                 dataset_id=dataset_id)
    total_time = time.time()
    threads_pool = [threading.Thread(target=etl.run) for thread in range(threads_count)]

    for thread in threads_pool:
        thread.start()
        time.sleep(1)

    for thread in threads_pool:
        thread.join()

    log_message("All threads finished! "
                "Processed {} records.".format(etl.processed))
    log_execution_time(total_time)
