from celery import group
from fastapi import APIRouter, BackgroundTasks, HTTPException
# from workers.tasks import invoke_lambda_task
from core.db import mongo_connector
from celery.result import GroupResult, AsyncResult

router = APIRouter()


@router.get("/result/{job_id}")
async def get_result(job_id: str):
    print("JOB ID: ", job_id)
    result = AsyncResult(job_id)
    if result.ready():
        messages = result.get()
        await mongo_connector.db.results.insert_one({"task_id" : str(result.task_id), "result" : messages})
        result.forget()
        return {"status": "completed", "messages": messages}
    else:
        return {"status": "pending"}