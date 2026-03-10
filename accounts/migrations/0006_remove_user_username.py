# Generated manually - Remove username field from User model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_user_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
