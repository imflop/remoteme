import json
import logging

from django.contrib import admin, messages
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from jobs.models import Advert, Scope, Stack
from jobs.tasks import calculate_similarity_coefficient
from utils.admin import CreateUpdateDateTimeAdvertAdmin

logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split("\n")]
            self.attrs["rows"] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs["cols"] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


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
    # formfield_overrides = {
    #     JSONField: {'widget': PrettyJSONWidget}
    # }

    list_display = (
        "id",
        "is_moderate",
        "similarity_coefficient",
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
    actions = ("recalculate_similarity_coefficient",)
    readonly_fields = ("similar_adverts_prettified",)
    exclude = ("similar_adverts",)

    def similar_adverts_prettified(self, instance=None):
        response = []
        if instance.similar_adverts:
            for sa in instance.similar_adverts:
                advert_id = sa["advert_id"]
                advert_ratio = sa["ratio"]
                url = reverse("admin:jobs_advert_change", args=[advert_id])
                response.append(f"<a href='{url}'>{advert_ratio * 100:.2f}% Similar with advert[{advert_id}]</a>")
        return mark_safe(response)

    similar_adverts_prettified.short_description = "similar adverts prettified"

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        t = type(fields)
        return fields + t(
            ("similarity_coefficient",),
        )

    def recalculate_similarity_coefficient(self, request, queryset):
        for item in queryset:
            calculate_similarity_coefficient.delay(item.id)
        self.message_user(request, _("Коэффициенты пересчитываются, это займет время"), messages.SUCCESS)

    recalculate_similarity_coefficient.short_description = _("Пересчитать коэффициент")
