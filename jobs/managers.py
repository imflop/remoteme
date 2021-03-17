from django.db.models import QuerySet


class AdvertManager(QuerySet):
    """
    Менеджер объявлений
    """

    def only_moderated(self):
        return self.prefetch_related("stack").select_related("scope").filter(is_moderate=True)
