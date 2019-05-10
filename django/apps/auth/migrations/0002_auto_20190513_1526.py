from django.db import migrations

def create_users(apps, schema_editor):
    import json
    from django.contrib.auth import get_user_model
    User = get_user_model()
    with open('sample_data_django.json') as f:
        data = json.load(f)
    User.objects.create_superuser(**data['defaultUser'])
    for user in data['users']:
        User.objects.create_user(**user)

class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0001_initial'),
    ]

    operations = [
                migrations.RunPython(create_users),
    ]
