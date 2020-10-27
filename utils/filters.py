from django.conf import settings
from django.forms import widgets
from django_filters import FilterSet


class StyledFilterSet(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.get_field_items():
            if isinstance(field.widget, widgets.Select):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'id': f'id_{field_name}_{self.__class__.__name__}'
                })
                field.empty_label = settings.EMPTY_CHOICE_LABEL

    def get_field_items(self):
        return self.form.fields.items()
