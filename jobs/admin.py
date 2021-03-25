from django.contrib import admin, messages
from django.utils.translation import gettext as _

from jobs.models import Advert, Scope, Stack
from jobs.tasks import calculate_similarity_coefficient
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

    def recalculate_similarity_coefficient(self, request, queryset):
        for item in queryset:
            calculate_similarity_coefficient.delay(item.id)
        self.message_user(request, _("Коэффициенты пересчитываются, это займет время"), messages.SUCCESS)

    recalculate_similarity_coefficient.short_description = _("Пересчитать коэффициент")
