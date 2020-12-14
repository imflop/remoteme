from uuid import uuid4
from django.db import models
from django.core.validators import MaxLengthValidator, EmailValidator
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext as _

from taggit.managers import TaggableManager
from unidecode import unidecode

from jobs.collections import LevelType, CurrencyType
from jobs.managers import AdvertManager
from utils.models import CreateUpdateDateTimeAbstract


class Scope(CreateUpdateDateTimeAbstract):
    title = models.CharField(
        verbose_name=_('Название'),
        max_length=64,
        validators=[MaxLengthValidator],
        help_text=_('Название специализации')
    )
    slug_title = models.SlugField(verbose_name=_('Слуг'), max_length=128)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Область работы')
        verbose_name_plural = _('Области работ')

    def __str__(self):
        return f'{self.title}'


class Advert(CreateUpdateDateTimeAbstract):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    short_description = models.CharField(
        verbose_name=_('Короткое описание'),
        max_length=128,
        validators=[MaxLengthValidator],
        help_text=_('Короткое и внятное описание кого вы ищете (макс. 128 символов)')
    )
    slug_short_description = models.SlugField(verbose_name=_('Слуг'), max_length=256)
    long_description = models.TextField(
        verbose_name=_('Полное описание вакансии'),
        max_length=1024,
        validators=[MaxLengthValidator],
        help_text=_('Подробно составленное объявление работает лучше, перечислите карьерные возмонжости, '
                    'миссию вашей компании, инженерную культуру компании, etc')
    )
    level = models.CharField(
        verbose_name=_('Уровень кандидата'),
        max_length=16,
        choices=LevelType.CHOICES,
        default=LevelType.JUNIOR
    )
    scope = models.ForeignKey(
        to='Scope',
        verbose_name=_('Область работы'),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        help_text=_('Облать работы или тип конкретной специализации кандидата')
    )
    salary_from = models.PositiveIntegerField(
        verbose_name=_('Зарплата от'),
        help_text=_('Уровень зарплаты от')
    )
    salary_to = models.PositiveIntegerField(
        verbose_name=_('Зарплата до'),
        help_text=_('Уровень зарплаты до'),
        blank=True,
        null=True
    )
    currency = models.CharField(
        verbose_name=_('Валюта'),
        max_length=16,
        choices=CurrencyType.CHOICES,
        default=CurrencyType.USD
    )
    company_name = models.CharField(
        verbose_name=_('Название компании'),
        max_length=256,
        validators=[MaxLengthValidator],
        help_text=_('Названик компании')
    )
    country = models.CharField(
        verbose_name=_('Страна'),
        max_length=128,
        validators=[MaxLengthValidator],
        blank=True,
        null=True,
        help_text=_('Страна')
    )
    city = models.CharField(
        verbose_name=_('Город'),
        max_length=128,
        validators=[MaxLengthValidator],
        blank=True,
        help_text=_('Город')
    )
    telegram = models.CharField(
        verbose_name=_('Телеграм'),
        max_length=128,
        validators=[MaxLengthValidator],
        blank=True,
        help_text=_('Обратная свзяь в телеграм')
    )
    email = models.EmailField(
        verbose_name=_('email'),
        validators=[EmailValidator],
        help_text=_('Электронная почта для обратной связи')
    )
    is_moderate = models.BooleanField(verbose_name=_('Модерация'), default=False)

    stack = TaggableManager(
        verbose_name=_('Технологический стэк'),
        help_text=_('Разделяемый запятой запрашиваемый стэк технологий')
    )

    objects = AdvertManager.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Объявление')
        verbose_name_plural = _('Объявления')

    def __str__(self):
        return f'{self.short_description}'

    def get_absolute_url(self):
        return reverse_lazy('jobs:detail', kwargs={
            'level': self.level,
            'uuid': self.uuid,
        })

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug_short_description = slugify(unidecode(self.short_description), allow_unicode=True)
        super().save(force_insert, force_update, using, update_fields)
