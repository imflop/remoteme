# Generated by Django 3.1.2 on 2020-10-19 22:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20201019_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]