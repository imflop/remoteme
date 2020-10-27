from django.conf import settings
from django.contrib.messages.api import error
from django.forms import widgets, Form, ModelForm


class StyledFromMixin:
    __excludable_widget_types = (
        widgets.FileInput,
        widgets.CheckboxInput,
        widgets.RadioSelect,
    )

    __form_control: str = 'form-control'
    __js_class_prefix: str = 'js-field_'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.get_field_items():

            css_class = field.widget.attrs.get('class', '')
            css_class += f'{self.__form_control} {self.__js_class_prefix}{field_name}'
            field.widget.attrs.update({'class': css_class})

            if isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({'rows': '6'})

            if isinstance(field.widget, widgets.Select) and hasattr(field, 'empty_label') and field.empty_label is not None:
                field.empty_label = settings.EMPTY_CHOICE_LABEL

    def get_field_items(self):
        return self.fields.copy().items()
    
    def is_valid(self):
        result = super().is_valid()
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result


class StyledModelForm(StyledFromMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StyledForm(StyledFromMixin, Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
