import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import TokenSerializer

pytestmark = pytest.mark.django_db


def test_users_imported_from_sample(sample_data, django_user_model):
    """ Should have imported all users from sample_data.json """
    assert len(sample_data['users']) == django_user_model.objects.count()


def test_has_a_admin_user(django_user_model, sample_data):
    """ Should have a user named `admin` there is a superuser """
    admin_pk = sample_data['defaultUser']['id']
    admin = django_user_model.objects.get(pk=admin_pk)
    assert admin.username == 'admin'
    assert admin.is_superuser and admin.is_staff


def test_jwt_user_login(client, sample_data):
    """ Should be able to login using username and password e get a token """
    admin = sample_data['defaultUser']
    data = {'username': admin['username'], 'password': admin['password']}
    resp = client.post('/api/auth/login', data, format='json')

    assert resp.status_code == status.HTTP_200_OK
    assert 'access' in resp.data
    assert 'refresh' in resp.data

    payload = AccessToken(resp.data.get('access'))
    for key, value in admin.items():
        if key == 'password':
            continue
        assert key in payload and payload[key] == value


def test_refresh_token(client, django_user_model, sample_data):
    """ Should be able to use the refresh token to get a new token """
    user = django_user_model.objects.get(pk=sample_data['defaultUser']['id'])
    refresh_token = TokenSerializer.get_token(user)
    resp = client.post(
        '/api/auth/refresh_token',
        {'refresh': str(refresh_token)},
        format='json',
    )
    assert resp.status_code == status.HTTP_200_OK
    assert 'access' in resp.data
    AccessToken(resp.data['access'])
