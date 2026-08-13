from celery import Celery

from config import Config


def make_celery():

    celery = Celery(

        "laboratory_forms",

        broker=Config.CELERY_BROKER_URL,

        backend=Config.CELERY_RESULT_BACKEND

    )

    celery.conf.update(

        task_serializer="json",

        accept_content=["json"],

        result_serializer="json",

        timezone="UTC",

        enable_utc=True,

        task_track_started=True,

        result_expires=3600

    )

    return celery


celery = make_celery()