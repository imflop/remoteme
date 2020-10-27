from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreateUpdateDateTimeAbstract(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата обновления'), auto_now=True, editable=False)

    class Meta:
        abstract = True
