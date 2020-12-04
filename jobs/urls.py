from django.urls import path


from jobs.views import (
    AdvertListView, AdvertSearchListView, AdvertStackListView, AdvertDetailView, AdvertCreateFormView, AutoResponseView
)

app_name = 'jobs'


urlpatterns = [
    path('', AdvertListView.as_view(), name='list'),
    path('search/', AdvertSearchListView.as_view(), name='search'),
    path('tag/<slug:stack_slug_name>/', AdvertStackListView.as_view(), name='stack'),
    path('jobs/create/', AdvertCreateFormView.as_view(), name='create'),
    path('jobs/auto-json', AutoResponseView.as_view(), name='auto-json'),
    path('<str:level>/<uuid:uuid>/', AdvertDetailView.as_view(), name='detail'),
]
