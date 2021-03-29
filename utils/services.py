import fnmatch
import os
import random
import re
from dataclasses import dataclass
from datetime import datetime

from jobs.collections import CurrencyType, LevelType
from jobs.models import Advert, Scope, Stack
from utils.dtos.hh import Item, KeySkill


def get_file_path() -> str:
    pattern = f"hh_{datetime.now().strftime('%Y%m%d')}_*.json"
    result = fnmatch.filter(os.listdir("/tmp"), pattern)
    return f"/tmp/{result[0]}" if result else ""


def get_stack_list(key_skills: list[KeySkill]) -> list[Stack]:
    result = []

    for k in key_skills:

        if Stack.objects.filter(name__iexact=k.name).exists():
            stack = Stack.objects.filter(name=k.name).first()
            result.extend([stack] if stack else [])
        else:
            stack, _ = Stack.objects.get_or_create(name=k.name)
            result.append(stack)

    return result


@dataclass
class AdvertService:
    """..."""

    CLEANER = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

    def init_advert(self, item: Item) -> Advert:
        cleaned_description = self._clean_from_html(item.description)

        return Advert(
            short_description=item.name,
            long_description=cleaned_description,
            level=self._get_level(item.name, cleaned_description),
            scope=self._get_scope(item.name, cleaned_description),
            salary_from=item.salary.from_value,
            salary_to=item.salary.to,
            currency=self._get_currency_type(item.salary.currency),
            company_name=item.employer.name,
            city=item.address.city if item.address else "",
            vacancy_source_url=item.alternate_url if item.alternate_url else "",
            telegram=item.contacts.phones[0] if item.contacts else "",
            email=item.contacts.email if item.contacts else "",
            is_moderate=False,
        )

    def _clean_from_html(self, raw_text: str) -> str:
        clean_text = ""

        if raw_text:
            clean_text = re.sub(self.CLEANER, "", raw_text)

        return clean_text

    def _get_level(self, name: str, description: str) -> str:
        level = ""

        for i in LevelType.ITEMS:
            if self._is_word_in_text(i, name):
                level = i
            elif self._is_word_in_text(i, description):
                level = i

        if not level:
            level = random.choice(LevelType.ITEMS)

        return level

    def _get_scope(self, name: str, description: str) -> Scope:
        scope_name = ""
        names = Scope.objects.all().values_list("title", flat=True)

        for n in names:
            if self._is_word_in_text(n, name):
                scope_name = n
            elif self._is_word_in_text(n, description):
                scope_name = n

        if not scope_name:
            scope_name = random.choice(names)

        scope = Scope.objects.filter(title=scope_name).first()
        return scope

    @staticmethod
    def _is_word_in_text(word: str, text: str) -> bool:
        matches = ""

        if text:
            pattern = r"(^|[^\w]){}([^\w]|$)".format(word)
            pattern = re.compile(pattern, re.IGNORECASE)
            matches = re.search(pattern, text)
        return bool(matches)

    @staticmethod
    def _get_currency_type(currency) -> str:
        result: str = CurrencyType.USD

        for i in CurrencyType.ITEMS:
            if i == currency.lower():
                result = i
            elif currency == "RUR":
                result = CurrencyType.RUB

        return result
