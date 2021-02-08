from django import template

from jobs.collections import CurrencyType

register = template.Library()


@register.simple_tag
def currency_icon(currency_name: str):
    return CurrencyType.get_icon_by_name(currency_name)
