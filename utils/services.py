import fnmatch
import os
import random
import re
from datetime import datetime
from typing import List, Optional, AnyStr

from taggit.models import Tag

from jobs.collections import LevelType
from jobs.models import Advert, Scope


class AdvertService:
    CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    def __init__(self, advert_item):
        self.item = advert_item
        self.advert = self._get_advert(self.item)
        self.stack_list = self._get_stack_list()

    @classmethod
    def get_file_path(cls) -> str:
        pattern = f"hh_{datetime.now().strftime('%Y-%m-%d')}*.json"
        result = fnmatch.filter(os.listdir("/tmp"), pattern)
        return f"/tmp/{result[0]}"

    def get_advert_object(self) -> Advert:
        return self.advert

    def get_stack_list(self) -> List[str]:
        return self.stack_list

    def _get_advert(self, data) -> Advert:
        text = self._clean_from_html(data.get('description'))
        return Advert(
            short_description=data.get('name') if data.get('name') else 'No Short Description',
            long_description=text,
            level=self._get_level(),
            scope=self._get_scope(),
            salary_from=self._get_salary('from'),
            salary_to=self._get_salary('to'),
            company_name=self._get_company_name(),
            city=self._get_city(),
            telegram='',
            email='email@email.not',
            is_moderate=False
        )

    def _get_level(self) -> str:
        level = ""
        for i in LevelType.ITEMS:
            if self._is_word_in_text(i, str(self.item.get('name'))):
                level = i
            elif self._is_word_in_text(i, str(self.item.get('description'))):
                level = i
        if not level:
            level = random.choice(LevelType.ITEMS)
        return level

    def _get_scope(self) -> Scope:
        name = ""
        names = Scope.objects.all().values_list('title', flat=True)
        for n in names:
            if self._is_word_in_text(n, self.item.get('name')):
                name = n
            elif self._is_word_in_text(n, self.item.get('description')):
                name = n
        scope = Scope.objects.filter(title=name).first()
        return scope

    def _get_salary(self, param: str) -> int:
        salary = 0
        if self.item.get('salary'):
            salary = {
                'from': self.item['salary'].get('from'),
                'to': self.item['salary'].get('to')
            }.get(param)
        return salary if salary else 0

    def _get_company_name(self) -> str:
        name = ""
        if self.item.get('employer'):
            name = self.item['employer'].get('name')
        return name

    def _get_city(self) -> str:
        name = ""
        if self.item.get('area'):
            name = self.item['area'].get('name')
        return name

    def _get_stack_list(self) -> List[str]:
        stack_list = []
        if self.item.get('key_skills'):
            stack_set = {s.get('name') for s in self.item.get('key_skills')}
            for stack in stack_set:
                if Tag.objects.filter(name__iexact=stack).exists():
                    tag = Tag.objects.filter(name=stack).first()
                    stack_list.extend([tag.name] if tag else [])
                else:
                    tag = Tag.objects.create(name=stack)
                    stack_list.append(tag.name)
        return stack_list

    def _clean_from_html(self, raw_text: str) -> str:
        clean_text = ""
        if raw_text:
            clean_text = re.sub(self.CLEANER, "", raw_text)
        return clean_text

    def _is_word_in_text(self, word: str, text: str) -> bool:
        matches = ""
        if text:
            pattern = r"(^|[^\w]){}([^\w]|$)".format(word)
            pattern = re.compile(pattern, re.IGNORECASE)
            matches = re.search(pattern, text)
        return bool(matches)