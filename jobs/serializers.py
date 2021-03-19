from rest_framework import serializers

from jobs.models import Advert, Stack, Scope


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ("title",)

    def to_representation(self, instance):
        return instance.title


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ("id", "name", "slug_name")

    def to_representation(self, instance):
        return instance.name


class AdvertSerializer(serializers.ModelSerializer):
    stack = StackSerializer(read_only=True, many=True)
    scope = ScopeSerializer(read_only=True)

    class Meta:
        model = Advert
        fields = ("uuid", "short_description", "created_at", "long_description", "stack", "scope")
