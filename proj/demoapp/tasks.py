# Create your tasks here
from time import sleep

# from demoapp.models import Widget

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(name="soma", bind=True)
def add(self, x, y):
    logger.info('Fazendo a soma...')
    sleep(5)
    return x + y


@shared_task(name="multiplica")
def mul(x, y):
    sleep(5)
    return x * y


@shared_task(name="soma_lista")
def xsum(*numbers):
    sleep(5)
    return sum(numbers)

# @shared_task
# def count_widgets():
#     return Widget.objects.count()
#
#
# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()
