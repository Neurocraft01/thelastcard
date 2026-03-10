# Generated manually - Update url_slug help_text (remove username reference)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_nfccard_url_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfccard',
            name='url_slug',
            field=models.SlugField(blank=True, help_text='Unique URL slug for public profile access (auto-generated)', unique=True),
        ),
    ]
