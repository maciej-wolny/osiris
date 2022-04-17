import pytest

import main


@pytest.fixture(scope="session")
def app():
    return main.app
