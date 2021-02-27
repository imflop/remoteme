from django.views.generic.base import ContextMixin


class PageMetaViewMixin(ContextMixin):
    """
    Миксимн для формирования меты на страницах
    """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(page_meta=dict(
            title="remoteme.dev поиск вакансий на удаленку",
            description="Remote programming job board поиск вакансий на удаленку"
        ))
        return context
