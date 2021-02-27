from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from django_select2.views import AutoResponseView

from jobs.models import Advert
from jobs.forms import AdvertCreateForm
from jobs.filters import AdvertFilter
from utils.mixins import PageMetaViewMixin
from utils.paginator import DiggPaginator


class AdvertBaseListView(ListView, PageMetaViewMixin):
    """
    Базовая view для вывода списка объявлений
    """
    model = Advert
    paginate_by = 23
    paginator_class = DiggPaginator
    template_name = 'jobs/list.html'

    def get_queryset(self):
        return super().get_queryset().only_moderated()


class AdvertFilterListView(AdvertBaseListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter'] = self.filterset
        return context


class AdvertListView(AdvertFilterListView):
    """
    Вывод списка объявлений по страницам
    """
    filterset_class = AdvertFilter


class AdvertSearchListView(AdvertFilterListView):
    """
    Простой поиск по объявлениям
    """
    filterset_class = AdvertFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        object_list = queryset.filter(Q(long_description__icontains=query))
        return object_list


class AdvertStackListView(AdvertFilterListView):
    filterset_class = AdvertFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        stack_slug_name = self.kwargs.get('stack_slug_name')
        context.update(dict(
            advert_list=Advert.objects.filter(stack__slug=stack_slug_name)
        ))
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
