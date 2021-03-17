from rest_framework import serializers

from jobs.models import Advert


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ("uuid", "short_description", "created_at", "long_description")
