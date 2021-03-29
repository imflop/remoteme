"""remoteme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.urls import include, path

from remoteme.sitemaps import AdvertSitemap

API_PREFIX = "api/v1/"
sitemaps = {"advert": AdvertSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_PREFIX}", include("jobs.urls")),
    path("sitemap.xml", sitemaps_views.index, {"sitemaps": sitemaps}),
    path(
        "sitemap-<section>.xml",
        sitemaps_views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
