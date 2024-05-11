from django.db import migrations

from account.models import User


def create_initial_user(apps, schema_editor):
    User.objects.create_superuser(
        username='admin',
        password='admin@jo316',
        name='Administrator',
        is_default=True
    )


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_user)
    ]
