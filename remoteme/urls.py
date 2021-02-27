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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import views as sitemaps_views

from remoteme.sitemaps import AdvertSitemap


sitemaps = {
    'advert': AdvertSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls')),
    path('', include('jobs.urls')),
    path('sitemap.xml', sitemaps_views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemaps_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
