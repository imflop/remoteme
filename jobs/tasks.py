import os
import json

from remoteme.celery_remoteme import app
from utils.services import AdvertService


@app.task()
def load_hh_data():
    if os.path.exists(AdvertService.get_file_path()):
        with open(AdvertService.get_file_path(), "r") as json_file:
            data = json.load(json_file)
            for item in data:
                service = AdvertService(item)
                advert = service.get_advert_object()
                advert.save()
                advert.stack.set(*service.get_stack_list())
                advert.save()
            msg = "Data are saved"
    else:
        msg = f"File on {AdvertService.get_file_path()} is not found"
    return msg
