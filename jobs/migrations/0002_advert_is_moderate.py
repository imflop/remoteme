# Generated by Django 3.1.2 on 2020-10-05 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='is_moderate',
            field=models.BooleanField(default=False, verbose_name='Модерация'),
        ),
    ]