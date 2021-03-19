from django.contrib import admin

from jobs.models import Scope, Stack, Advert
from utils.admin import CreateUpdateDateTimeAdvertAdmin


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = (
        "id",
        "title",
    )
    search_fields = ("title",)
    prepopulated_fields = {"slug_title": ("title",)}


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin):
    list_display = ("name", "slug_name")
    search_fields = ("name",)
    prepopulated_fields = {"slug_name": ("name",)}


@admin.register(Advert)
class AdvertAdmin(CreateUpdateDateTimeAdvertAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "is_moderate",
        "short_description",
        "created_at",
        "level",
        "scope",
        "currency",
        "salary_from",
        "salary_to",
        "company_name",
        "city",
        "updated_at",
        "uuid",
    )
    list_display_links = ("id", "short_description")
    list_filter = ("created_at", "scope", "is_moderate")
    prepopulated_fields = {"slug_short_description": ("short_description",)}
    search_fields = ("id", "short_description", "company_name", "scope__title")
    filter_horizontal = ("stack",)
