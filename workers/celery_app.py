# workers/celery_app.py
from celery import Celery
from core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend = f"mongodb+srv://johnybotways:johnybotways@cluster0.yeoq0b1.mongodb.net/{settings.MONGODB_DB}?retryWrites=true&w=majority",
    mongodb_backend_settings={
        'database': settings.MONGODB_DB,  # Your database name
        'taskmeta_collection': 'results',  # Optional: Custom collection name
    },
)

celery_app.autodiscover_tasks(["workers.tasks"])

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Kolkata',
    enable_utc=True,
    result_expires = 60
)
