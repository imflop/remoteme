import django_filters

from jobs.models import Advert


class AdvertFilter(django_filters.FilterSet):
    class Meta:
        model = Advert
        fields = ("scope",)
