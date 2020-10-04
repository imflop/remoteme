# Generated by Django 3.1.1 on 2020-09-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(choices=[('MAX_VIP_ADVERTS', 'Максимальное колличество VIP объявлений'), ('MAX_PIN_ADVERTS', 'Максимальное колличество PIN объявлений'), ('MAX_SIDEBAR_COMMENTS', 'Максимально колличество коментариев в сайдбаре'), ('ADVERTS_PER_PAGE', 'Колличество объявлений на странице'), ('BLOG_POST_PER_PAGE', 'Колличество постов блога на странице'), ('BLOG_LIST_PAGE_TITLE', 'Заголовок (title) для страницы списка статей')], default='MAX_VIP_ADVERTS', max_length=128, unique=True, verbose_name='Ключ')),
                ('value', models.CharField(blank=True, max_length=128, verbose_name='Значение')),
                ('value_type', models.CharField(choices=[('number', 'Число'), ('number_float', 'Число с запятой'), ('string', 'Строка'), ('boolean', 'Флаг')], default='string', max_length=16, verbose_name='Тип значения')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]
