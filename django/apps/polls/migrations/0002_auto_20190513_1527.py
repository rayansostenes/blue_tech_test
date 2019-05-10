from django.db import migrations

def _get_data(key=None):
    import json
    with open('sample_data_django.json') as f:
        data = json.load(f)
    return data.get(key) or None

def create_objects(model, key):
    def create(apps, schema_editor):
        Model = apps.get_model('polls', model)
        for obj in _get_data(key):
            Model.objects.create(**obj)
    return create


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
        ('my_auth', '0002_auto_20190513_1526'),
    ]

    operations = [
        migrations.RunPython(create_objects('Poll', 'polls')),
        migrations.RunPython(create_objects('Choice', 'choices')),
        migrations.RunPython(create_objects('Vote', 'votes')),
    ]
