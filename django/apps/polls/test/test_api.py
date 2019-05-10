import pytest

from rest_framework import status
from .helpers import get_votes_dict, auth_headers
from lib.sample_data import import_sample_data

pytestmark = pytest.mark.django_db

POLL_ID = '0839beb8-0b42-4eff-98c1-d1052101938a'
POLLS_API = '/api/polls/'
RESULTS_URL = f'{POLLS_API}{POLL_ID}/results/'
ADMIN_PK = '6f0cc701-4f3b-484a-8906-b59d52024a61'

def test_polls_api_needs_auth(client):
    """ Only authenticated user can view the polls api """
    resp = client.get(POLLS_API, format='json')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in resp.data

def test_results_api_needs_auth(client):
    """ Only authenticated user can view the results api """
    resp = client.get(RESULTS_URL, format='json')
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in resp.data

def test_results_api(client, django_user_model, sample_data):
    """ Should return the results for a poll """
    admin = django_user_model.objects.get(pk=ADMIN_PK)
    resp = client.get(RESULTS_URL, format='json', **auth_headers(admin))
    sample_results = get_votes_dict(sample_data['votes'].values(), POLL_ID)
    assert sample_results == resp.data

# @pytest.mark.django_db(transaction=True)
def test_results_api_no_vote(client, django_user_model):
    """ Should return the results for a poll """
    new_user = django_user_model.objects.create_user('new_user', '123')
    resp = client.get(RESULTS_URL, format='json', **auth_headers(new_user))
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    assert 'detail' in resp.data
