from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from users.managers import UserManager


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = models.CharField(verbose_name=_("username"), max_length=150, blank=True)
    email = models.EmailField(verbose_name=_("email address"), unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f"{self.email}"
