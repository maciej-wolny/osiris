import json
import xmltodict

from zeep import Client
from zeep.exceptions import Fault

from src.config import BaseConfig


class ApiCEIDG:
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.url = BaseConfig.API_CEIDG_URL

    def search_by_registration_date(self, start_date, end_date):
        """Required date format: YYYY-MM-DD"""
        request_data = {'AuthToken': BaseConfig.API_CEIDG_TOKEN,
                        'DateFrom': start_date,
                        'DateTo': end_date
                        }
        client = Client(self.url)
        with client.settings(xml_huge_tree=True):
            try:
                response = xmltodict.parse(client.service.GetMigrationData201901(**request_data))
            except Fault as error:
                response = error.detail
        return response


if __name__ == '__main__':
    RESULT = ApiCEIDG().search_by_registration_date('2018-03-01', '2018-03-01')

    with open('../processing/result3.json', 'w') as fp:
        json.dump(RESULT, fp)
