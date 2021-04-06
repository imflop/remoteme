import typing as t

from jobs.models import Advert, Stack
from jobs.tasks import calculate_similarity_coefficient


def create_advert(data: t.OrderedDict) -> Advert:
    input_stack = data.pop("stack")
    new_advert = Advert.objects.create(**data)
    for s in input_stack:
        stack, created = Stack.objects.get_or_create(name=s)
        # TODO: change to unpack list new_advert.add(*[list_with_stack])
        if created:
            new_advert.stack.add(stack.pk)
        else:
            new_advert.stack.add(stack.pk)

    new_advert.save()
    calculate_similarity_coefficient.delay(new_advert.pk)

    return new_advert
