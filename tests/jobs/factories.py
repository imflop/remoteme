import factory

from jobs.models import Scope


class ScopeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Scope
        django_get_or_create = ("title",)

    title = factory.Sequence(lambda t: "Title %d" % t)
    title_slug = factory.LazyAttribute(lambda s: s.title)
