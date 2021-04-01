import os

import httpx
from django.db import transaction
from pydantic import parse_obj_as

from django.conf import settings

from jobs.models import Advert
from remoteme.celery_remoteme import app
from utils.dtos.hh import Item
from utils.services import AdvertService, get_stack_list


if settings.DEBUG:
    GRABBERS_HOST = "localhost"
else:
    GRABBERS_HOST = os.environ.get("GRABBERS_HOST")


@app.task()
def load_hh_data():
    headers = {"user-agent": "remoteme/1.0.1"}
    r = httpx.get(f"http://{GRABBERS_HOST}:8888/hh", timeout=20, headers=headers)

    if r.status_code == 200:
        count = 0
        data = r.json()
        service = AdvertService()

        for d in data:
            item_object = parse_obj_as(Item, d)

            if item_object.salary:
                if (
                        item_object.salary.from_value
                        and item_object.salary.from_value > 0
                        and item_object.salary.to
                        and item_object.salary.to > 0
                ):
                    count += 1

                    with transaction.atomic():
                        advert = service.init_advert(item_object)
                        advert.save()

                        if item_object.key_skills:
                            advert.stack.add(*get_stack_list(item_object.key_skills))
                            advert.save()

                        calculate_similarity_coefficient.delay(advert.pk)

        msg = f"{count} items are saved"

    else:
        msg = f"Error while getting data {r.status_code}: {r.text}"

    return msg


@app.task(autoretry_for=(Exception,), max_retries=1)
def calculate_similarity_coefficient(adv_id: int) -> str:
    advert = Advert.objects.filter(pk=adv_id).first()
    msg = f"Advert by id {adv_id} not found"

    if advert:
        similar_adverts = Advert.get_similar_adverts(advert.pk, advert.long_description)

        if similar_adverts:
            max_similarity_coefficient = max(list(map(lambda x: x.similarity, similar_adverts)))
            ids_and_ratios = [dict(advert_id=sa.id, ratio=sa.similarity) for sa in similar_adverts]
            advert.similarity_coefficient = float(max_similarity_coefficient)
            advert.similar_adverts = ids_and_ratios
            advert.save()
        else:
            advert.is_moderate = True
            advert.similarity_coefficient = 0.123
            advert.save()

        msg = f"Advert={advert.pk} was saved with ratio={advert.similarity_coefficient}"

    return msg
