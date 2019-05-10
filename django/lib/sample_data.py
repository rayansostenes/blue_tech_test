import os
import json
from django.contrib.auth import get_user_model
from apps.polls.models import Poll, Choice, Vote

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
SAMPLE_DATA_FILE = os.path.join(BASE_DIR, 'sample_data.json')

User = get_user_model()


def _list_to_dict(lst):
    return {d['id']: d for d in lst}


def import_sample_data():
    with open(SAMPLE_DATA_FILE) as f:
        data = json.load(f)
    users = create_users(data['users'], data['defaultUser'])
    polls = create_polls(data['polls'])
    votes = create_votes(data['votes'])

    return {
        'defaultUser': data['defaultUser'],
        'users': users,
        'polls': polls,
        'votes': votes,
    }


def create_votes(votes):
    votes_kw = []
    for vote in votes:
        new_vote = {}
        for key, value in vote.items():
            if not key.endswith('id'):
                key = f'{key}_id'
            new_vote[key] = value
        votes_kw.append(new_vote)

    Vote.objects.bulk_create([Vote(**kw) for kw in votes_kw])
    return _list_to_dict(votes)


def create_choices(choices, poll_id):
    for choice in choices:
        choice['image_url'] = choice.pop('imageUrl', '')
        choice['poll_id'] = poll_id
    Choice.objects.bulk_create([Choice(**kw) for kw in choices])
    return _list_to_dict(choices)


def create_polls(polls):
    polls = [(p.pop('choices', []), p) for p in polls]
    Poll.objects.bulk_create([Poll(**kw) for _, kw in polls])
    return {
        poll['id']: {
            **poll, 'choices': create_choices(choices, poll['id'])
        }
        for choices, poll in polls
    }


def _get_user_dict(user):
    base = {k: user.get(k) for k in ['id', 'email', 'username', 'password']}
    return {
        **base,
        'first_name': user.get('firstName'),
        'last_name': user.get('lastName'),
        'is_staff': user.get('isAdmin'),
    }


def create_users(users, super_user):
    for user in users:
        User.objects.create_user(**_get_user_dict(user))
    super_user = _get_user_dict(super_user)
    User.objects.create_superuser(**super_user)
    return _list_to_dict([super_user] + users)
