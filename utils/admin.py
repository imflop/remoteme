class CreateUpdateDateTimeAdvertAdmin:
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        t = type(fieldsets)
        return fieldsets + t(((None, {"fields": (("created_at", "updated_at"),)}),))

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        t = type(fields)
        return fields + t(
            ("created_at", "updated_at"),
        )
