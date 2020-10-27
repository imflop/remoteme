from os import name
from django.urls import path

from django_filters.views import FilterView

from jobs.views import AdvertListView, AdvertDetailView, AdvertCreateFormView, AutoResponseView
from jobs.models import Advert

app_name = 'jobs'


urlpatterns = [
    path('', AdvertListView.as_view(), name='list'),
    path('', FilterView.as_view(model=Advert), name='filter'),
    path('jobs/create/', AdvertCreateFormView.as_view(), name='create'),
    path('jobs/auto-json', AutoResponseView.as_view(), name='auto-json'),
    path('<str:level>/<uuid:uuid>/', AdvertDetailView.as_view(), name='detail'),
]
