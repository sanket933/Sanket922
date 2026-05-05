from celery import Celery
from app.core.config import get_settings

settings = get_settings()
celery_app = Celery('company_os', broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(task_acks_late=True, worker_prefetch_multiplier=1, task_default_retry_delay=60)
