from os import getenv

celery_broker = getenv('CELERY_BROKER')
celery_backend = getenv('CELERY_BACKEND')