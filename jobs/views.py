from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from django_select2.views import AutoResponseView

from jobs.models import Advert
from jobs.forms import AdvertCreateForm
from jobs.filters import AdvertFilter


class AdvertListView(ListView):
    model = Advert
    template_name = 'jobs/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter'] = AdvertFilter(self.request.GET, queryset=self.get_queryset())
        return context


class AdvertDetailView(DetailView):
    model = Advert
    query_pk_and_slug = True
    template_name = 'jobs/detail.html'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        advert = get_object_or_404(Advert, uuid=uuid)
        return advert


class AdvertCreateFormView(FormView):
    model = Advert
    form_class = AdvertCreateForm
    template_name = 'jobs/create.html'
    success_url = reverse_lazy('jobs:create')
    success_message = 'Ваше объявление успешно добавлено и проходит процедуру модерации'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        form.save()
        return super().form_valid(form)


class TagAutoResponseView(AutoResponseView):
    pass
