from django.urls import path

from jobs.views import (AdvertCreateView, AdvertDetailView, AdvertListView,
                        ScopeListView, StackListView)

app_name = "jobs"


urlpatterns = [
    path("adverts/list", AdvertListView.as_view(), name="list"),
    path("adverts/<uuid:uuid>", AdvertDetailView.as_view(), name="detail"),
    path("adverts/create", AdvertCreateView.as_view(), name="create"),
    path("scope/list", ScopeListView.as_view(), name="scope-list"),
    path("stack/list", StackListView.as_view(), name="stack-list"),
]
