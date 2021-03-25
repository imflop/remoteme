from rest_framework import serializers

from jobs.models import Advert, Scope, Stack


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
        fields = (
            "uuid",
            "short_description",
            "created_at",
            "stack",
            "scope",
            "salary_from",
            "salary_to",
            "city",
            "company_name",
            "currency",
            "is_moderate",
        )
