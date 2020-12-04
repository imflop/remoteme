from random import randint, choice

from django.core.management.base import BaseCommand

from faker import Faker
from taggit.models import Tag

from jobs.collections import LevelType
from jobs.models import Advert, Scope


class Command(BaseCommand):
    help = 'Generate data for manual testing'

    def __init__(self):
        super().__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        scopes = Scope.objects.all().values_list('id', flat=True)
        for i in range(101):
            advert = self._generated_advert(scopes)
            advert.save()
            advert.stack.set(*[f"{Tag.objects.get_or_create(name=self.fake.word())[0]}" for _ in range(5)])
            advert.save()

    def _generated_advert(self, scopes: list) -> Advert:
        scope = Scope.objects.get(pk=choice(scopes))
        return Advert(
            short_description=self.fake.text(randint(45, 100)),
            long_description=self.fake.text(1000),
            level=choice(LevelType.ITEMS),
            scope=scope,
            salary_from=self.fake.pyint(1490, 2900, 250),
            salary_to=self.fake.pyint(3000, 6000, 250),
            company_name=self.fake.company(),
            country=self.fake.country(),
            city=self.fake.city(),
            telegram='@telegram',
            email=self.fake.company_email(),
            is_moderate=self.fake.pybool(),
        )
