from celery import Celery

from src.config.settings import settings

CELERY_BROKER_URL = settings.REDIS.redis_celery_url
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

celery_app = Celery(
    "Lynx",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_persistent=True,
    retry_backoff=True,
    retry_jitter=True,
    broker_connection_retry_on_startup=True,
    retry_policy={
        "max_retries": 5,
        "interval_start": 10,
        "interval_step": 5,
        "interval_max": 500,
    },
)
