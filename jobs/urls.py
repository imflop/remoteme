from django.urls import path


from jobs.views import (
    AdvertListView,
)

app_name = "jobs"


urlpatterns = [
    path("adverts/list", AdvertListView.as_view(), name="list"),
]
