from rest_framework import serializers

from jobs.collections import LevelType
from jobs.models import Advert, Scope, Stack


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ("id", "title")


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ("id", "name", "slug_name")


class ScopeFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ("title",)

    def to_representation(self, instance):
        return instance.title


class StackFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ("name",)

    def to_representation(self, instance):
        return instance.name


class AdvertSerializer(serializers.ModelSerializer):
    stack = StackFlatSerializer(read_only=True, many=True)
    scope = ScopeFlatSerializer(read_only=True)

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


class AdvertDetailSerializer(serializers.ModelSerializer):
    stack = StackFlatSerializer(read_only=True, many=True)
    scope = ScopeFlatSerializer(read_only=True)

    class Meta:
        model = Advert
        fields = (
            "short_description",
            "long_description",
            "created_at",
            "stack",
            "scope",
            "salary_from",
            "salary_to",
            "city",
            "company_name",
            "currency",
        )


class AdvertCreateSerializer(serializers.Serializer):
    short_description = serializers.CharField(required=True)
    long_description = serializers.CharField(required=True)
    level = serializers.ChoiceField(choices=LevelType.CHOICES, required=True)
    scope = serializers.PrimaryKeyRelatedField(queryset=Scope.objects.all(), required=True, write_only=True)
    salary_from = serializers.IntegerField(required=True)
    salary_to = serializers.IntegerField()
    stack = serializers.ListSerializer(child=serializers.CharField(allow_blank=False), required=True)
    company_name = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    telegram = serializers.CharField()
    email = serializers.CharField()
