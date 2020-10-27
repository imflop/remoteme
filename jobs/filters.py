from utils.filters import StyledFilterSet
from jobs.models import Advert


class AdvertFilter(StyledFilterSet):

    class Meta:
        model = Advert
        fields = ('level', 'scope',)
