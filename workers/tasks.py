import requests
from celery import signals
from datetime import datetime
import asyncio
from celery.signals import task_postrun, task_success
from celery.utils.log import get_task_logger
from workers.celery_app import celery_app
from core import settings
logger = get_task_logger(__name__)

@celery_app.task(
    name="workers.tasks.invoke_lambda_task",
    bind=True,
    max_retries=3,
    acks_late=True,
    time_limit=120,
    soft_time_limit=110
)

# @celery_app.task(name="workers.tasks.invoke_lambda_task", bind=True, max_retries=3)
# async def invoke_lambda_task_async(self):
#     try:
#         print("Invoking Lambda...")
#         response = requests.get(settings.LAMBDA_URL, timeout=120)
#         response.raise_for_status()
#         data = response.json()
#         data_message = data.get("message", {})
#         if data_message:
#             print("Saving Data in Mongo",data_message)
#             await mongo_connector.db.results.insert_one({"result" : data_message})
#         return data_message
#     except Exception as e:
#         print("Error:", e)
#         raise self.retry(exc=e, countdown=5 * (self.request.retries + 1))
    
@celery_app.task(name="workers.tasks.invoke_lambda_task", bind=True, max_retries=3)
def invoke_lambda_task(self):
    try:
        print("Invoking Lambda...")
        response = requests.get(settings.LAMBDA_URL, timeout=120)
        response.raise_for_status()
        data = response.json()
        data_message = data.get("message", {})

        return data_message
    except Exception as e:
        print("Error:", e)
        raise self.retry(exc=e, countdown=5 * (self.request.retries + 1))


# async def save_task_result_async(task_id, result_data):
#     try:
#         async with get_mongo_connection() as db:
#             collection = db["responses"]
#             document = {
#                 "task_id": task_id,
#                 "result": result_data,
#                 "timestamp": datetime.now(),
#                 "status": "completed"
#             }
#             await collection.insert_one(document)
#     except Exception as e:
#         print(f"Error saving task result: {e}")
#         raise

# def run_async(coro):
#     """Helper to run async code from sync context"""
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         return loop.run_until_complete(coro)
#     finally:
#         loop.close()
#         asyncio.set_event_loop(None)

@task_success.connect
def on_task_success(sender=None, result=None, **kwargs):
    """Signal handler for successful task completion"""
    if result is None:
        return
    
    task_id = sender.request.id if sender else None
    print(f"Task : {sender.name} completed!, result: {result}")
    print("\nTask Id: ", task_id)
#     if not task_id:
#         return
    
#     # Run the async save operation
#     run_async(save_task_result_async(task_id, result))

# @signals.task_success.connect
# def task_success(sender = None, result=None, **kwargs):
#     print(f"Task : {sender.name} completed!, result: {result}")


# async def save_task_result_async(task_id, result_data):
#     try:
#         async with mongo_connector.db as db:
#             collection = db["responses"]
#             document = {
#                 "task_id": task_id,
#                 "result": result_data,
#                 "timestamp": datetime.now(),
#                 "status": "completed"
#             }
#             await collection.insert_one(document)
#     except Exception as e:
#         print(f"Error saving task result: {e}")
#         raise

# def run_async(coro):
#     """Helper to run async code from sync context"""
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         return loop.run_until_complete(coro)
#     finally:
#         loop.close()
#         asyncio.set_event_loop(None)

# @task_success.connect
# def on_task_success(sender=None, result=None, **kwargs):
#     """Signal handler for successful task completion"""
    
#     if result is None:
#         return
    
#     task_id = sender.request.id if sender else None
#     print("saving completed task:  ", task_id)
#     if not task_id:
#         return
    
#     # Run the async save operation
#     run_async(save_task_result_async(task_id, result))