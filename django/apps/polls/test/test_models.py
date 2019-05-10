import pytest
from rest_framework_simplejwt.tokens import AccessToken

from apps.polls.models import Poll, Choice, Vote

from .helpers import get_votes_dict, POLL_ID, ADMIN_PK, PAULA_PK

pytestmark = pytest.mark.django_db


def test_polls_imported_from_sample(sample_data):
    """ Should have imported all polls from sample_data.json """
    assert len(sample_data['polls']) == Poll.objects.count()


def test_choices_imported_from_sample(sample_data):
    """ Should have imported all choices from sample_data.json """
    len_choices = sum(len(p['choices']) for p in sample_data['polls'].values())
    assert len_choices == Choice.objects.count()


def test_votes_imported_from_sample(sample_data):
    """ Should have imported all votes from sample_data.json """
    assert len(sample_data['votes']) == Vote.objects.count()


def test_vote_results(sample_data):
    """ results() method should return the right value """
    poll = Poll.objects.get(pk=POLL_ID)
    sample_results = get_votes_dict(sample_data['votes'].values(), POLL_ID)
    db_results = {
        str(id): votes
        for id, votes in poll.results().values_list('id', 'votes')
    }
    assert sample_results == db_results


def test_user_has_voted(django_user_model):
    """ Should return a boolean to indicate if the user has voted  """
    poll = Poll.objects.get(pk=POLL_ID)
    admin = django_user_model.objects.get(pk=ADMIN_PK)
    paula = django_user_model.objects.get(pk=PAULA_PK)
    assert not poll.user_has_voted(admin)
    assert poll.user_has_voted(paula)


def test_vote_method(django_user_model, sample_data):
    """ Should add a vote to a choice """
    admin = django_user_model.objects.get(pk=ADMIN_PK)
    poll = Poll.objects.get(pk=POLL_ID)
    poll.vote(admin, 'b1eb1d75-0f56-4f97-913b-eb7074b79236')
    assert len(sample_data['votes']) + 1 == Vote.objects.count()
