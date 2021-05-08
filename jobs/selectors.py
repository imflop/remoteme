import typing as t
import uuid

from django.core.cache import cache

from jobs.filters import AdvertFilter
from jobs.models import Advert, Scope, Stack


def get_scope() -> t.Iterable[Scope]:
    key = f"{get_stack.__qualname__}:scope_list"
    scopes = cache.get(key)

    if not scopes:
        scopes = Scope.objects.all()
        cache.set(key, scopes, 60)

    return scopes


def get_stack() -> t.Iterable[Stack]:
    key = f"{get_stack.__qualname__}:stack_list"
    stacks = cache.get(key)

    if not stacks:
        stacks = Stack.objects.all()
        cache.set(key, stacks, 60)

    return stacks


def get_adverts(*, filters=None) -> t.Iterable[Advert]:
    filters = filters or {}

    qs = Advert.objects.only_moderated()

    return AdvertFilter(filters, qs).qs


def get_advert(*, fetched_by: uuid) -> t.Optional[Advert]:
    return Advert.objects.filter(uuid=fetched_by).first()
