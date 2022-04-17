import json

import requests
from flask import current_app as app

from src.models.rejestrio_record import RejestrIoRecord

MISSING_VALUE = "N/A"


def create_request_data_to_rejestrio():
    """Create url, headers and search_params for Rejestrio request."""
    headers = {'Authorization': app.config['REJESTR_IO_KEY']}
    search_params = {'chapter': 'basic'}
    return headers, search_params


def court_letters_size(district_court):
    """Change district court's letters size.

    This function changes `SĄD REJONOWY DLA KRAKOWA-ŚRÓDMIEŚCIA W KRAKOWIE` to
    `Sąd Rejonowy dla Krakowa-Śródmieścia w Krakowie`.
    """
    words_to_replace = {
        'W': 'w',
        'Dla': 'dla',
        'We': 'we'
    }

    def replace_word(word):
        if word in words_to_replace.keys():
            return words_to_replace[word]
        return word

    district_court = district_court.lower().title()
    if "M. St." in district_court:
        district_court = district_court.replace("M. St.", "m. st.")
    district_court = [replace_word(word) for word in district_court.split()]
    district_court = [word.upper()
                      if word.startswith(('I', 'X', 'V'))
                      else word for word in district_court]
    district_court = " ".join(district_court)
    return district_court


def company_name_letters_size(company_name):
    """Change company name's letters size.

    This function changes `WIELKA KAZACHSKA SPÓŁKA GIEŁDOWA` to
    `Wielka Kazachska spółka giełdowa`.
    """
    company_name = company_name.lower()
    if 'spółka' in company_name:
        company_name = company_name.split('spółka')
        company_name = f"{company_name[0].title()}spółka{company_name[1]}"
    return company_name


def get_financial_data(krs_no):
    """Fetch financial data from Rejestrio.

    There is no shared_capital and fully_paid_up info in the data.
    This function gets missing data from Rejestrio.
    """
    url = f"{app.config['REJESTR_IO_BASE_URL']}/krs/{krs_no.lstrip('0')}"
    headers, search_params = create_request_data_to_rejestrio()
    try:
        response = requests.get(url=url,
                                headers=headers,
                                params=search_params) \
            .json()['fields']
        return response
    except (KeyError, TypeError):
        return MISSING_VALUE


def get_shared_capital_data(response):
    """Fetch additional data from Rejestrio.

    There is no shared_capital and fully_paid_up info in the data.
    This function gets missing data from Rejestrio.
    """
    try:
        response = response['wysokosc_kapitalu_zakladowego']['_value']
        amount, currency = response["amount"], response["currency"]
        amount = f"{amount:,}".replace(',', '.')
        shared_capital = f"{amount},00 {currency.lower()}"
        return shared_capital
    except (KeyError, TypeError):
        return MISSING_VALUE


def get_fully_paid_up_info(response):
    """Get if shared capital fully_paid_up info from Rejestrio.

    Return MISSING_VALUE when there is no data in Rejestrio.
    """
    try:
        paid_up = response["kwotowe_okreslenie_czesci_kapitalu_wplaconego"]["_value"]['amount']
        shared_capital = response['wysokosc_kapitalu_zakladowego']['_value']['amount']
        fully_paid_up = (int(paid_up) == int(shared_capital))
        return "(opłaconym w całości)" if fully_paid_up else "(nie opłaconym w całości)"
    except (KeyError, TypeError):
        return MISSING_VALUE


def missing_shared_capital(name):
    """Return info about missing shared_capital variable."""
    return f"W rejestio nie ma kapitału zakładowego dla {name}"


def missing_fully_paid_up_info(name):
    """Return info about missing fully_paid_up variable."""
    return f"W rejestio nie ma informacji o tym, czy kapitał zakładowy jest " \
           f"w pełni opłacony dla: {name}"


def missing_financial_response(name):
    """Return info about missing financial data."""
    return f"Simplify nie znalazł informacji w rejestrio dla: {name}"


def create_spolka_zoo(record):
    """Create commencement of Spolka zoo."""
    response = get_financial_data(record.krs)
    if response == MISSING_VALUE:
        return missing_financial_response(record.name), False
    record.shared_capital = get_shared_capital_data(response)
    if record.shared_capital == MISSING_VALUE:
        return missing_shared_capital(record.name), False
    return f"{record.company_name}, siedziba: {record.address.city}, adres: ul. " \
           f"{record.address.street} {record.address.house_no}, {record.address.code} " \
           f"{record.address.city}, wpisana do rejestru przedsiębiorców, prowadzonego przez " \
           f"{record.district_court}, pod numerem KRS: {record.krs}, NIP: {record.nip} i " \
           f"REGON: {record.regon}, o kapitale zakładowym w wysokości {record.shared_capital}, " \
           f"reprezentowaną przez: \v\v[--] - [--]", True


def create_spolka_akcyjna(record):
    """Create commencement of Spolka akcyjna."""
    response = get_financial_data(record.krs)
    if response == MISSING_VALUE:
        return missing_financial_response(record.name), False
    record.shared_capital = get_shared_capital_data(response)
    if record.shared_capital == MISSING_VALUE:
        return missing_shared_capital(record.name), False
    record.fully_paid_up = get_fully_paid_up_info(response)
    if record.fully_paid_up == MISSING_VALUE:
        return missing_fully_paid_up_info(record.name), False
    return f"{record.company_name}, siedziba: {record.address.city}, adres: ul. " \
           f"{record.address.street} {record.address.house_no}, {record.address.code} " \
           f"{record.address.city}, wpisana do rejestru przedsiębiorców, prowadzonego przez " \
           f"{record.district_court}, pod numerem KRS: {record.krs}, NIP: {record.nip} i " \
           f"REGON: {record.regon}, o kapitale zakładowym w wysokości {record.shared_capital}  " \
           f"{record.fully_paid_up}, reprezentowaną przez: \v\v[--] - [--]", True


def create_spolka_komandytowa(record):
    """Create commencement of Spolka komandytowa."""
    return f"{record.company_name}, siedziba: {record.address.city}, adres: ul. " \
           f"{record.address.street} {record.address.house_no}, {record.address.code} " \
           f"{record.address.city}, wpisana do rejestru przedsiębiorców, prowadzonego przez " \
           f"{record.district_court}, pod numerem KRS: {record.krs}, NIP: {record.nip} i " \
           f"REGON: {record.regon}, reprezentowaną przez: \v\v[--] - [--]", True


def create_komandytowo_akcyjna(record):
    """Create commencement of Spolka komandytowo-akcyjna."""
    response = get_financial_data(record.krs)
    if response == MISSING_VALUE:
        return missing_financial_response(record.name), False
    record.shared_capital = get_shared_capital_data(response)
    if record.shared_capital == MISSING_VALUE:
        return missing_shared_capital(record.name), False
    record.fully_paid_up = get_fully_paid_up_info(response)
    if record.fully_paid_up == MISSING_VALUE:
        return missing_fully_paid_up_info(record.name), False
    return f"{record.company_name}, siedziba: {record.address.city}, adres: ul. " \
           f"{record.address.street} {record.address.house_no}, {record.address.code} " \
           f"{record.address.city}, wpisana do rejestru przedsiębiorców, prowadzonego przez " \
           f"{record.district_court}, pod numerem KRS: {record.krs}, NIP: {record.nip} i " \
           f"REGON: {record.regon}, o kapitale zakładowym w wysokości {record.shared_capital} " \
           f"{record.fully_paid_up}, reprezentowaną przez: \v\v[--] - [--]", True


def create_fundacja(record):
    """Create commencement of Fundacja."""
    return f"{record.company_name}, siedziba: {record.address.city}, adres: ul. " \
           f"{record.address.street} {record.address.house_no}, {record.address.code} " \
           f"{record.address.city}, wpisana do rejestru stowarzyszeń, prowadzonego przez " \
           f"{record.district_court}, pod numerem KRS: {record.krs}, NIP: {record.nip} i " \
           f"REGON: {record.regon}, reprezentowaną przez: \v\v[--] - [--]", True


LEGAL_FORMS_DICT = {
    "SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ": create_spolka_zoo,
    "SPÓŁKA AKCYJNA": create_spolka_akcyjna,
    "SPÓŁKA KOMANDYTOWA": create_spolka_komandytowa,
    "SPÓŁKA KOMANDYTOWO-AKCYJNA": create_spolka_akcyjna,
    "SPÓŁKA JAWNA": create_spolka_komandytowa,
    "FUNDACJA": create_fundacja,
    "SPÓŁKA PARTNERSKA": create_spolka_komandytowa,
}


def get_district_court_data(krs_no):
    """Fetch district_court data from Rejestrio.

    There is no district_court, shared_capital and fully_paid_up info in the data.
    This function gets missing data from Rejestrio.
    """
    url = f"{app.config['REJESTR_IO_BASE_URL']}/krs/{krs_no.lstrip('0')}/entries"
    headers, search_params = create_request_data_to_rejestrio()
    try:
        response = requests.get(url=url,
                                headers=headers,
                                params=search_params) \
            .json()
        if response[0].get('court', False):
            district_court = response[0]['court']
        elif response[-1].get('court', False):
            district_court = response[-1]['court']
        else:
            return MISSING_VALUE

        return court_letters_size(district_court)
    except KeyError:
        return MISSING_VALUE


def from_krs_record(record: RejestrIoRecord):
    """Modify record's values, get additional data and create proper commencement."""
    if record.__class__.__name__ != "RejestrIoRecord":
        return json.dumps({'results': f"PODANE WYSZUKIWANIE NIE JEST INSTANCJĄ RejestrIoRecord"})
    if record.name != MISSING_VALUE:
        record.company_name = company_name_letters_size(record.name)
    else:
        return json.dumps({'results': f"SPÓŁKA NIE MA NAZWY, JEJ KRS: {record.krs}"})
    record.district_court = get_district_court_data(record.krs)
    if record.district_court == MISSING_VALUE:
        return json.dumps({'results': f"SIMPLIFY NIE ZNALAZŁ SĄDU REJONOWEGO: {record.name}"})
    get_commencement = LEGAL_FORMS_DICT.get(record.legal_form, None)
    if get_commencement is None:
        return json.dumps({
            'results':
                f"SIMPLIFY NIE ZNALAZŁ KOMPARYCJI DLA PODANEJ FORMY SPÓŁKI: "
                f"{record.legal_form}"})
    commencement, successful = get_commencement(record)
    if successful:
        return json.dumps({'results': commencement}, ensure_ascii=False)
    return json.dumps(
        {'results': f"SIMPLIFY NIE MÓGŁ STWORZYĆ KOMPARYCJI, POWÓD: {commencement}"})
