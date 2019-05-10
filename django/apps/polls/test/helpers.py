from rest_framework_simplejwt.tokens import AccessToken

POLL_ID = '0839beb8-0b42-4eff-98c1-d1052101938a'
POLLS_API = '/api/polls/'
RESULTS_URL = f'{POLLS_API}{POLL_ID}/results/'
ADMIN_PK = '6f0cc701-4f3b-484a-8906-b59d52024a61'
PAULA_PK = '3e23de00-f824-435f-bf0b-2d2deac8f61c'

def get_votes_dict(votes, poll_id):
    results = {}
    for vote in votes:
        if vote.get('poll') != poll_id: # pragma: no cover
            continue
        choice_id = vote.get('choice')
        results[choice_id] = results.get(choice_id, 0) + 1
    return results

def auth_headers(user):
    token = AccessToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
