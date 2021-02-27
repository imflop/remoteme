from django.contrib import sitemaps

from jobs.models import Advert


class AdvertSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = "daily"
    limit = 10000

    def items(self):
        return Advert.objects.filter(is_moderate=True)

    def lastmod(self, obj):
        return obj.created_at
