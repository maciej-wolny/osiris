from flask import Flask
from flask_cors import CORS

from src.config import configure_app
from src.routes.krs_records import KRS_RECORDS
from src.routes.commencement import GET_COMMENCEMENT
from src.routes.users import USERS
from src.routes.trigger import TRIGGER

app = Flask(__name__)
app.register_blueprint(KRS_RECORDS)
app.register_blueprint(TRIGGER)
app.register_blueprint(GET_COMMENCEMENT)
app.register_blueprint(USERS)
CORS(app)
configure_app(app)


@app.errorhandler(500)
def handle_500(error):
    """Handle error."""
    return str(error), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

