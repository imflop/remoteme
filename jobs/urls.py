from django.urls import path


from jobs.views import (
    AdvertListView, AdvertDetailView
)

app_name = "jobs"


urlpatterns = [
    path("adverts/list", AdvertListView.as_view(), name="list"),
    path("adverts/<uuid:uuid>", AdvertDetailView.as_view(), name="detail"),
]
