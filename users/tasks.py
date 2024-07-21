from celery import shared_task

from users.services import activ_sub, cleaner_key


@shared_task
def activ_subs():
    activ_sub()


@shared_task
def cleaner_keys():
    cleaner_key()
