from zeep import Client
import xmltodict

from src.config import BaseConfig


class ApiRegon:
    def __init__(self):
        self.session_key = None
        self.url = BaseConfig.API_REGON_BASE_URL
        self._connect_to_api_regon()

    def _connect_to_api_regon(self):
        """Creates ApiRegon session and stores session_key"""
        self.client = Client(self.url)
        login_data = {'pKluczUzytkownika': BaseConfig.API_REGON_TOKEN}
        self.session_key = self.client.service.Zaloguj(**login_data)
        self.client.transport.session.headers.update({'sid': self.session_key})

    def search_by_regon(self, regon_number):
        """Searches ApiRegon by REGON number."""
        request_data = {'pParametryWyszukiwania': {'pRegon': regon_number}}
        result = self.client.service.DaneSzukajPodmioty(**request_data)
        return xmltodict.parse(result)

    def get_full_report(self, regon_number, report_type):
        """Gets full company report for specified REGON."""
        request_data = {'pRegon': regon_number,
                        'pNazwaRaportu': report_type}
        result = self.client.service.DanePobierzPelnyRaport(**request_data)
        return xmltodict.parse(result)

    def get_changes(self, date, report_type):
        """Gets REGON numbers for which data has changes in specified date for
        specified report-type"""
        request_data = {'pDataRaportu': date,
                        'pNazwaRaportu': report_type}
        result = self.client.service.DanePobierzRaportZbiorczy(**request_data)
        return xmltodict.parse(result)
