from django.contrib import admin

from jobs.models import Scope, Advert
from utils.admin import CreateUpdateDateTimeAdvertAdmin


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug_title': ('title',)}


@admin.register(Advert)
class AdvertAdmin(CreateUpdateDateTimeAdvertAdmin, admin.ModelAdmin):
    list_display = (
        'id', 'is_moderate', 'short_description', 'created_at', 'level', 'scope', 'currency',
        'salary_from', 'salary_to', 'company_name', 'tech_stack', 'city', 'updated_at', 'uuid'
    )
    list_display_links = ('id', 'short_description')
    list_filter = ('created_at', 'scope')
    prepopulated_fields = {'slug_short_description': ('short_description',)}
    search_fields = ('id', 'short_description', 'company_name', 'scope__title')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('stack')

    def tech_stack(self, obj) -> str:
        return ", ".join({o.name for o in obj.stack.all()})

