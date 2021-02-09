from django import forms

from django_select2.forms import ModelSelect2TagWidget
from taggit.models import Tag

from jobs.models import Advert
from utils.forms import StyledModelForm


class StackModelSelect2TagWidget(ModelSelect2TagWidget):
    queryset = Tag.objects.all()
    search_fields = ('name__icontains',)

    def value_from_datadict(self, data, files, name) -> str:
        """
        Создаем новые таги если их нет в бд. Возвращаем форматированную пробелами строку для
        корректной работы парсера taggit (очень лень было писать свой парсер для форматирования строки)
        """
        values = set(super().value_from_datadict(data, files, name))
        cleaned_values = self.queryset.filter(
            **{'pk__in': [v for v in values if v.isdigit()]}
        ).values_list('name', flat=True)
        existed_values = list(cleaned_values)

        for value in values:
            if not value.isdigit():
                obj, created = self.queryset.get_or_create(name=value)
                if created:
                    existed_values.append(obj.name)

        return ''.join(f'"{c}"' if c == existed_values[-1] else f'"{c}" ' for c in existed_values)


class AdvertCreateForm(StyledModelForm):
    """
    Форма создания объявления
    """

    class Meta:
        model = Advert
        fields = ('short_description', 'long_description', 'level', 'scope', 'salary_from', 'salary_to',
                  'stack', 'company_name', 'country', 'city', 'telegram', 'email')
        widgets = {
            'short_description': forms.TextInput(attrs={'placeholder': 'Короткое описание'}),
            'long_description': forms.Textarea(attrs={'placeholder': 'Подробное описание'}),
            'level': forms.Select(),
            'scope': forms.Select(),
            'salary_from': forms.TextInput(),
            'salary_to': forms.TextInput(),
            'stack': StackModelSelect2TagWidget(data_view='jobs:auto-json'),
            'company_name': forms.TextInput(),
            'country': forms.TextInput(),
            'city': forms.TextInput(),
            'telegram': forms.TextInput(),
            'email': forms.EmailInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
