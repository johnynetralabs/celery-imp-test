from workers.celery_app import celery_app
import requests
import traceback
from core.config import settings

@celery_app.task(bind=True, max_retries=3)
def invoke_lambda_task(self):
    try:
        response = requests.get(settings.LAMBDA_URL, timeout=90)
        data = response.json()
        return {
            "success": True,
            "result": data,
            "task_id": self.request.id
        }
    except Exception as e:
        self.retry(exc=e)
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
