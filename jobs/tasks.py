import os
import json

from remoteme.celery_remoteme import app
from utils.services import AdvertService


@app.task()
def load_hh_data():
    if os.path.exists(AdvertService.get_file_path()):
        with open(AdvertService.get_file_path(), "r") as json_file:
            data = json.load(json_file)
            count = len(data)
            for item in data:
                service = AdvertService(item)
                advert = service.get_advert_object()
                if advert.salary_from > 0 and advert.salary_to > 0:
                    advert.save()
                    advert.stack.set(*service.get_stack_list())
                    advert.save()
                    count -= 1
            msg = f"{count} items are saved"
    else:
        msg = f"File by {AdvertService.get_file_path()} is not found"
    return msg
