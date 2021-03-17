from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.utils import str2bool


class KeyItem:
    """
    Фабрика настроек
    Возвращает значения настройки по ключу
    """

    MAX_VIP_ADVERTS: str = "MAX_VIP_ADVERTS"
    MAX_PIN_ADVERTS: str = "MAX_PIN_ADVERTS"
    MAX_VIP_ADVERTS_PERIOD: str = "MAX_VIP_ADVERTS_PERIOD"
    MAX_PIN_ADVERTS_PERIOD: str = "MAX_PIN_POST_PERIOD"
    ADD_VIP_ADVERTS: str = "ADD_VIP_POST"
    MAX_SIDEBAR_COMMENTS: str = "MAX_SIDEBAR_COMMENTS"
    ADVERTS_PER_PAGE: str = "ADVERTS_PER_PAGE"
    BLOG_POST_PER_PAGE: str = "BLOG_POST_PER_PAGE"

    ITEMS = (
        MAX_VIP_ADVERTS,
        MAX_PIN_ADVERTS,
        MAX_VIP_ADVERTS_PERIOD,
        MAX_PIN_ADVERTS_PERIOD,
        ADD_VIP_ADVERTS,
        MAX_SIDEBAR_COMMENTS,
        ADVERTS_PER_PAGE,
        BLOG_POST_PER_PAGE,
    )

    CHOICES = (
        (MAX_VIP_ADVERTS, "Максимальное колличество VIP объявлений"),
        (MAX_PIN_ADVERTS, "Максимальное колличество PIN объявлений"),
        (MAX_SIDEBAR_COMMENTS, "Максимально колличество коментариев в сайдбаре"),
        (ADVERTS_PER_PAGE, "Колличество объявлений на странице"),
        (BLOG_POST_PER_PAGE, "Колличество постов блога на странице"),
    )


class ValuesType:
    """
    Тип значения
    """

    NUMBER = "number"  # Число
    NUMBER_FLOAT = "number_float"  # Число с запятой
    STRING = "string"  # Строка
    BOOLEAN = "boolean"  # Флаг

    ITEMS = (
        NUMBER,
        NUMBER_FLOAT,
        STRING,
        BOOLEAN,
    )

    CHOICES = (
        (NUMBER, "Число"),
        (NUMBER_FLOAT, "Число с запятой"),
        (STRING, "Строка"),
        (BOOLEAN, "Флаг"),
    )

    @classmethod
    def get_type_func(cls, value_type):
        return {cls.NUMBER: int, cls.NUMBER_FLOAT: float, cls.STRING: str, cls.BOOLEAN: str2bool}.get(value_type)


class Settings(models.Model):
    """
    Модель настроек
    """

    key = models.CharField(
        verbose_name=_("Ключ"), max_length=128, unique=True, choices=KeyItem.CHOICES, default=KeyItem.MAX_VIP_ADVERTS
    )
    value = models.CharField(verbose_name=_("Значение"), max_length=128, blank=True)
    value_type = models.CharField(
        verbose_name=_("Тип значения"), max_length=16, choices=ValuesType.CHOICES, default=ValuesType.STRING
    )

    class Meta:
        verbose_name = _("Настройка")
        verbose_name_plural = _("Настройки")

    def __str__(self):
        return f"Параметр: {self.key}, Значение: {self.value}"

    @classmethod
    def get_value(cls, key: str, convert: bool = True):
        setting = cls.objects.filter(key=key).first()  # type: Settings
        if setting:
            if convert:
                type_func = ValuesType.get_type_func(setting.value_type)
                return type_func(setting.value)
            return setting.value
        return None
