import pytest
from lib.sample_data import import_sample_data

SAMPLE_DATA = {}

@pytest.fixture
def sample_data():
    return SAMPLE_DATA

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        data = import_sample_data()
        SAMPLE_DATA.update(data)