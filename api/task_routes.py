from celery import group
from fastapi import APIRouter, BackgroundTasks, HTTPException
from workers.tasks import invoke_lambda_task
from core.db import mongo_connector
from celery.result import GroupResult
router = APIRouter()


@router.get("/lambdas/{n}")
async def trigger_lambdas(n: int):
    job = group(invoke_lambda_task.s() for _ in range(n))()
    
    # Save job ID in MongoDB for later tracking
    await mongo_connector.db.tasks.insert_one({
        "job_id": job.id,
        "num_tasks": n,
        "task_ids": [t.id for t in job.children],
        "status": "submitted"
    })
    
    return {
        "message": f"{n} lambda tasks submitted", 
        "job_id": job.id,
        "task_ids": [t.id for t in job.children]
    }

# async def test_func():
#     lambda_invoke = invoke_lambda_task()
#     print("lambda_invoke: ", lambda_invoke)